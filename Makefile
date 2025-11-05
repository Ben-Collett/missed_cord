# Makefile for building libxkbwrap.so

CC       := gcc
CFLAGS   := -Wall -Wextra -O2 -fPIC $(shell pkg-config --cflags xkbcommon)
LDFLAGS  := -shared $(shell pkg-config --libs xkbcommon)
TARGET   := libxkbwrap.so
SRC      := xkbwrapper.c
OBJ      := $(SRC:.c=.o)

.PHONY: all clean rebuild

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CC) -o $@ $^ $(LDFLAGS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJ) $(TARGET)

rebuild: clean all
