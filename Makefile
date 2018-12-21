##
## EPITECH PROJECT, 2018
## SEC
## File description:
## Makefile
##

all:
	cp src/* .

clean:
	rm -f challenge*

fclean:
	rm -f challenge*

re: fclean all

.PHONY: all clean fclean re
