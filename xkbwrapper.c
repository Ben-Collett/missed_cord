// xkbwrap.c  (updated)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <xkbcommon/xkbcommon-names.h> // for XKB_MOD_NAME_*
#include <xkbcommon/xkbcommon.h>

static struct xkb_context *ctx = NULL;
static struct xkb_keymap *keymap = NULL;
static struct xkb_state *state = NULL;

/* cached modifier indices (or XKB_MOD_INVALID) */
static xkb_mod_index_t mod_shift = XKB_MOD_INVALID;
static xkb_mod_index_t mod_ctrl = XKB_MOD_INVALID;
static xkb_mod_index_t mod_alt = XKB_MOD_INVALID;
static xkb_mod_index_t mod_level3 =
    XKB_MOD_INVALID; /* optional, AltGr / Level3 */

/* Initialize XKB with a given layout (e.g. "us") */
int xkb_init(const char *layout) {
  ctx = xkb_context_new(XKB_CONTEXT_NO_FLAGS);
  if (!ctx)
    return 0;

  struct xkb_rule_names names = {.rules = "evdev",
                                 .model = "pc105",
                                 .layout = layout ? layout : "us",
                                 .variant = "",
                                 .options = ""};

  keymap = xkb_keymap_new_from_names(ctx, &names, XKB_KEYMAP_COMPILE_NO_FLAGS);
  if (!keymap) {
    xkb_context_unref(ctx);
    ctx = NULL;
    return 0;
  }

  /* cache modifier indices safely */
  mod_shift = xkb_keymap_mod_get_index(keymap, XKB_MOD_NAME_SHIFT);
  mod_ctrl = xkb_keymap_mod_get_index(keymap, XKB_MOD_NAME_CTRL);
  mod_alt =
      xkb_keymap_mod_get_index(keymap, XKB_MOD_NAME_ALT); // usually "Mod1"
  mod_level3 = xkb_keymap_mod_get_index(
      keymap, XKB_VMOD_NAME_LEVEL3); // "LevelThree" (AltGr)

  state = xkb_state_new(keymap);
  if (!state) {
    xkb_keymap_unref(keymap);
    xkb_context_unref(ctx);
    ctx = NULL;
    keymap = NULL;
    return 0;
  }

  return 1;
}

/* Set modifier state manually.
   We build depressed mask only if index != XKB_MOD_INVALID to avoid UB
*/
void xkb_set_modifiers(int shift, int ctrl, int alt) {
  if (!state || !keymap)
    return;

  xkb_mod_mask_t depressed = 0;

  if (shift && mod_shift != XKB_MOD_INVALID)
    depressed |= (1u << mod_shift);

  if (ctrl && mod_ctrl != XKB_MOD_INVALID)
    depressed |= (1u << mod_ctrl);

  /* note: "alt" here corresponds to XKB_MOD_NAME_ALT (usually Mod1).
     If you want AltGr (Level3) use a separate flag and mod_level3. */
  if (alt && mod_alt != XKB_MOD_INVALID)
    depressed |= (1u << mod_alt);

  /* pass latched/locked = 0, and layout depressed/latched/locked = 0 */
  /* Prototype: xkb_state_update_mask(state, depressed, latched, locked,
   * depressed_layout, latched_layout, locked_layout) */
  xkb_state_update_mask(state, depressed, 0, 0, 0, 0, 0);
}

/* small helper struct returned to python */
struct xkb_key_lookup {
  int keycode;
  uint32_t modifiers; // xkb_mod_mask_t fits in uint32_t on normal platforms
};

/* Convert a keycode + current state to UTF-8
   Returns malloc'd string — caller must free()
*/
char *xkb_translate_key(int keycode) {
  if (!state)
    return NULL;

  char buffer[64];
  int n = xkb_state_key_get_utf8(state, keycode, buffer, sizeof(buffer));
  if (n <= 0)
    return NULL;

  char *out = malloc(n + 1);
  if (!out)
    return NULL;

  strcpy(out, buffer);
  return out;
}

void xkb_cleanup() {
  if (state)
    xkb_state_unref(state);
  if (keymap)
    xkb_keymap_unref(keymap);
  if (ctx)
    xkb_context_unref(ctx);
  state = NULL;
  keymap = NULL;
  ctx = NULL;
}
