CFLAGS=$(shell pkg-config --cflags python-2.7)
SRC=$(wildcard *.c)
OBJ=$(SRC:.c=.so)

.PHONY: all
all: $(OBJ)


%.so: %.c
	$(CC) -o $@ -fPIC -shared -fstack-protector $(CFLAGS) $< 

