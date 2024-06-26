#!/usr/bin/python3
"""Module for the entry point of the command interpreter."""
import cmd
import sys
import shlex
import re
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Command interpreter class."""

    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity, 'Review': Review
    }

    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
        'number_rooms': int, 'number_bathrooms': int,
        'max_guest': int, 'price_by_night': int,
        'latitude': float, 'longitude': float
    }

    def preloop(self):
        """Print if isatty is false."""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax."""
        _cmd = _cls = _id = _args = ''  # initialize line elements

        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:
            _cls = line[:line.find('.')]
            _cmd = line[line.find('.') + 1:line.find('(')]
            _id = line[line.find('(') + 1:line.find(')')].split(', ')
            _id = _id[0].replace('\"', '')
            _args = ' '.join(_id[1:])
        except IndexError:
            pass

        return '{} {} {} {}'.format(_cmd, _cls, _id, _args)

    def do_quit(self, arg):
        """Quit command to exit the program."""
        exit()

    def help_quit(self):
        """Prints the help documentation for quit command."""
        print("Quit command to exit the program\n")

    def do_EOF(self, arg):
        """Handles End Of File character."""
        print()
        exit()

    def help_EOF(self):
        """Prints the help documentation for EOF command."""
        print("EOF command to exit the program\n")

    def emptyline(self):
        """Overrides the default behavior of repeating the last command."""
        pass

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it (to the JSON file) and prints the id."""
        if not arg:
            print("** class name missing **")
            return
        args = shlex.split(arg)
        class_name = args[0]
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        new_instance = HBNBCommand.classes[class_name]()
        for param in args[1:]:
            key_value = param.split('=')
            if len(key_value) != 2:
                continue

            key, value = key_value
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1].replace('_', ' ').replace('\\"', '"')
            elif '.' in value:
                try:
                    value = float(value)
                except ValueError:
                    continue
            else:
                try:
                    value = int(value)
                except ValueError:
                    continue

            setattr(new_instance, key, value)

        new_instance.save()
        print(new_instance.id)

    def help_create(self):
        """Prints the help documentation for create command."""
        print("Creates a new instance of BaseModel, saves it (to the JSON file) and prints the id\n")

    def do_show(self, arg):
        """Prints the string representation of an instance based on the class name and id."""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = args[0] + '.' + args[1]
        try:
            print(storage.all()[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """Prints the help documentation for show command."""
        print("Prints the string representation of an instance based on the class name and id\n")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id (save the change into the JSON file)."""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = args[0] + '.' + args[1]
        try:
            del(storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """Prints the help documentation for destroy command."""
        print("Deletes an instance based on the class name and id (save the change into the JSON file)\n")

    def do_all(self, arg):
        """Prints all string representation of all instances based or not on the class name."""
        args = shlex.split(arg)
        objects = storage.all()
        if not args:
            print([str(obj) for obj in objects.values()])
        elif args[0] in HBNBCommand.classes:
            print([str(obj) for obj in objects.values() if obj.__class__.__name__ == args[0]])
        else:
            print("** class doesn't exist **")

    def help_all(self):
        """Prints the help documentation for all command."""
        print("Prints all string representation of all instances based or not on the class name\n")

    def do_update(self, arg):
        """Updates an instance based on the class name and id by adding or updating attribute (save the change into the JSON file)."""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = args[0] + '.' + args[1]
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(args) == 2:
            print("** attribute name missing **")
            return
        if len(args) == 3:
            print("** value missing **")
            return

        obj = storage.all()[key]
        setattr(obj, args[2], eval(args[3]))
        obj.save()

    def help_update(self):
        """Prints the help documentation for update command."""
        print("Updates an instance based on the class name and id by adding or updating attribute (save the change into the JSON file)\n")

if __name__ == "__main__":
    HBNBCommand().cmdloop()

