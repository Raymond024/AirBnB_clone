#!/usr/bin/python3
"""
entry point for the command interpreter module

"""
from models import storage
import re
import json
import cmd
from models.base_model import BaseModel

class HBNBCommand(cmd.Cmd):
    """command interpreter class"""

    def user_error(self, line, num):
        """Displays error message

        Args:
            line: gets user input
            num: number of input arguments

        Description:
            Displays output to user

        """
        classes = ["BaseModel", "User", "State", "City",
                   "Amenity", "Place", "Review"]

        mesg = ["** class name missing **",
               "** class doesn't exist **",
               "** instance id missing **",
               "** no instance found **",
               "** attribute name missing **",
               "** value missing **"]
        if not line:
            print(mesg[0])
            return 1
        args = line.split()
        if num >= 1 and args[0] not in classes:
            print(mesg[1])
            return 1
        elif num == 1:
            return 0
        if num >= 2 and len(args) < 2:
            print(mesg[2])
            return 1
        d = storage.all()

        for x in range(len(args)):
            if args[x][0] == '"':
                args[x] = args[x].replace('"', "")
        key = args[0] + '.' + args[1]
        if num >= 2 and key not in d:
            print(mesg[3])
            return 1
        elif num == 2:
            return 0
        if num >= 4 and len(args) < 3:
            print(mesg[4])
            return 1
        if num >= 4 and len(args) < 4:
            print(mesg[5])
            return 1
        return 0

    def quit_cmd(self, line):
        """Handles the 'quit' command

        Args:
            line(args): input argument for quiting
            the terminal

        """
        return True

    def eof_cmd(self, line):
        """Quits command interpreter with ctrl+d

         Args:
            line(args): input argument for quiting
            the terminal

        """
        return True

    def line_empty(self, line):
        """
        Eliminates empty lines
        """
        return False

    def inst_create(self, line):
        """Creates a new instance of @cls_name class,
        and prints the new instance's ID.

        Args:
            line(args): Arguments to enter with command: <class name>
            Example: 'create User'

        """
        if (self.my_errors(line, 1) == 1):
            return
        args = line.split(" ")

        """
        args[0] contains class name, create new instance
        of that class updates 'updated_at' attribute,
        and saves into JSON file
        """
        obj = eval(args[0])()
        obj.save()

        print(obj.id)

    def do_show(self, line):
        """Prints a string representation of an instance.

        Args:
            line(line): to enter with command <class name> <id>
            Example: 'show User 1234-1234-1234'

        """
        if (self.my_errors(line, 2) == 1):
            return
        args = line.split()
        d = storage.all()
        if args[1][0] == '"':
            args[1] = args[1].replace('"', "")
        key = args[0] + '.' + args[1]
        print(d[key])

    def do_destroy(self, line):
        """Deletes an instance of a certain class.

        Args:
            line(args): to enter with command: <class name> <id>
            Example: 'destroy User 1234-1234-1234'

        """
        if (self.user_errors(line, 2) == 1):
            return
        args = line.split()
        d = storage.all()
        if args[1][0] == '"':
            args[1] = args[1].replace('"', "")
        key = args[0] + '.' + args[1]
        del d[key]
        storage.save()

    def all_inst(self, line):
        """Shows all instances, or instances of a certain class

        Args:
            line(args): enter with command (optional): <class name>
            Example: 'all' OR 'all User'

        """
        d = storage.all()
        if not line:
            print([str(i) for i in d.values()])
            return
        args = line.split()
        if (self.user_errors(line, 1) == 1):
            return
        print([str(w) for w in d.values()
               if w.__class__.__name__ == args[0]])

    def inst_update(self, line):
        """Updates an instance based on the class name
        and id by adding or updating an attribute

        Args:
            line(args): receives the commands:
            <class name> <id> <attribute name> "<attribute value>"
            Example: 'update User 1234-1234-1234 my_name "Bob"'

        """
        if (self.user_errors(line, 4) == 1):
            return
        args = line.split()
        d = storage.all()
        for x in range(len(args[1:]) + 1):
            if args[x][0] == '"':
                args[x] = args[x].replace('"', "")
        key = args[0] + '.' + args[1]
        attr_a = args[2]
        attr_b = args[3]
        try:
            if attr_a.isdigit():
                attr_b = int(attr_v)
            elif float(attr_b):
                attr_b = float(attr_b)
        except ValueError:
            pass
        class_attr = type(d[key]).__dict__
        if attr_a in class_attr.keys():
            try:
                attr_a = type(class_attr[attr_a])(attr_b)
            except Exception:
                print("Entered wrong type")
                return
        setattr(d[key], attr_a, attr_b)
        storage.save()

    def inst_count(self, class_n):
        """
        Method counts instances of a certain class
        """
        count_inst = 0
        for inst_object in storage.all().values():
            if inst_object.__class__.__name__ == class_n:
                count_inst += 1
        print(count_inst)

    def default(self, line):
        """Method to take care of following commands:
        <class name>.all()
        <class name>.count()
        <class name>.show(<id>)
        <class name>.destroy(<id>)
        <class name>.update(<id>, <attribute name>, <attribute value>)
        <class name>.update(<id>, <dictionary representation)

        Description:
            Creates a list representations of functional models
            Then use the functional methods to implement user
            commands, by validating all the input commands

        """
        names = ["BaseModel", "User", "State", "City", "Amenity",
                 "Place", "Review"]

        commands = {"all": self.do_all,
                    "count": self.my_count,
                    "show": self.do_show,
                    "destroy": self.do_destroy,
                    "update": self.do_update}

        args = re.match(r"^(\w+)\.(\w+)\((.*)\)", line)
        if args:
            args = args.groups()
        if not args or len(args) < 2 or args[0] not in names \
                or args[1] not in commands.keys():
            super().default(line)
        return

        if args[1] in ["all", "count"]:
            commands[args[1]](args[0])
        elif args[1] in ["show", "destroy"]:
            commands[args[1]](args[0] + ' ' + args[2])
        elif args[1] == "update":
            params = re.match(r"\"(.+?)\", (.+)", args[2])
            if params.groups()[1][0] == '{':
                dic_p = eval(params.groups()[1])
                for k, v in dic_p.items():
                    commands[args[1]](args[0] + " " + params.groups()[0] +
                                      " " + k + " " + str(v))
            else:
                rest = params.groups()[1].split(", ")
                commands[args[1]](args[0] + " " + params.groups()[0] + " " +
                                  rest[0] + " " + rest[1])


if __name__ == '__main__':
    cli = HBNBCommand()
    cli.cmdloop()
