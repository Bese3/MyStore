#!/usr/bin/python3

"""Defines the console."""
import cmd
from mods import dbstorage
from mods.book import Book
from mods.friend import Friend
from mods.hobby import Hobby
from mods.movie import Movie
from mods.music import Music
from mods.portifolio import Portfolio
from mods.user import User


class StoreCommand(cmd.Cmd):
    """The console program starts here"""
    prompt = "(store) "
    __classes = {
     'Book': Book,
     'Friend': Friend,
     'Hobby': Hobby,
     'Movie': Movie,
     'Music': Music,
     'Portfolio': Portfolio,
     'User': User
    }

    def emptyline(self):
        """Empty line + Enter will just return the prompt without any error.
        i.e. the prompt will not execute the previous command"""
        pass

    def do_quit(self, arg):
        """Exit the console: quit
        """
        return True

    def do_EOF(self, arg):
        """Exit the console: EOF
        """
        print("")
        return True

    def do_create(self, args):
        """ Create an object of any class"""
        if not args:
            print("** class name missing **")
        args = args.replace("=", ":")
        args = args.split(" ")
        if args[0] not in StoreCommand.__classes.keys():
            print("** class doesn't exist **")
            return
        new_instance = StoreCommand.__classes[args[0]]()
        for i in args[1:]:
            i = i.split(":")
            # if hasattr(new_instance, i[0]):
            setattr(new_instance, i[0],
                    i[1].replace("\"", "").replace("_", " "))
        if type(new_instance) is Friend:
            new_instance.friend_valid()
        # print(new_instance)
        new_instance.save()
        # storage.save()
        print(new_instance.id)

    def do_show(self, args):
        """`show` Usage: show <class> <id>
        Display the string representation of a class instance."""
        args = args.split(" ")
        if len(args) == 1 and args == ['']:
            print("** class name missing **")
            return
        if args[0] not in self.__classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        try:
            if args[0] + "." + eval(args[1]) not in\
                 dbstorage.all().keys():
                print("** no instance found **")
                return
            print(dbstorage.all()[args[0] + "." + eval(args[1])])
        except Exception:
            if args[0] + "." + args[1] not in dbstorage.all().keys():
                print("** no instance found **")
                return
            print(dbstorage.all()[args[0] + "." + args[1]])

    def do_destroy(self, args):
        """`destroy` Usage: destroy <class> <id>
        Delete a class instance of a given id."""
        args = args.split(" ")
        if len(args) == 1 and args == ['']:
            print("** class name missing **")
            return
        if args[0] not in self.__classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
            # if args[0] + "." + eval(args[1]) not in\
            #      dbstorage.all().keys():
            #     print("** no instance found **")
            #     return
            # dbstorage.delete()[args[0] + "." + eval(args[1])]
            # # del dbstorage.all()[args[0] + "." + eval(args[1])]
            # dbstorage.save()
        if args[0] + "." + args[1] not in dbstorage.all().keys():
            print("** no instance found **")
            return
        dbstorage.delete(dbstorage.all()[args[0] + "." + args[1]])
        # del dbstorage.all()[args[0] + "." + args[1]]
        dbstorage.save()

    def do_all(self, args):
        """`all`Usage: all or all <class>
        Display string representations of all instances of a given class."""

        args = args.split(" ")
        if args == ['']:
            objs = [i.__str__() for i in dbstorage.all().values()]
            print(objs)
            return
        if args[0] not in self.__classes and args != ['']:
            print("** class doesn't exist **")
            return
        objs = [i.__str__() for i in dbstorage.all().values() if
                i.to_json()["__class__"] == args[0]]
        print(objs)

    def do_update(self, args):
        """`update`
        update <class name> <id> <attribute name> "<attribute value>"
        Updates current instance of a class."""
        args = args.split(" ")
        if len(args) == 1 and args == ['']:
            print("** class name missing **")
            return
        if args[0] not in self.__classes.keys():
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        if len(args) == 2:
            print("** attribute name missing **")
            return
        if len(args) == 3:
            print("** value missing **")
            return
        try:
            if args[0] + "." + eval(args[1]) not in\
                 dbstorage.all().keys():
                print("** no instance found **")
                return
            obj = dbstorage.all()[args[0] + "." + eval(args[1])]
        except Exception:
            if args[0] + "." + args[1] not in dbstorage.all().keys():
                print("** no instance found **")
                return
            obj = dbstorage.all()[args[0] + "." + args[1]]
        if args[2][0] == "{":
            i = 2
            my_dict = ""
            while i < len(args):
                my_dict += args[i]
                if i != len(args) - 1:
                    my_dict += " "
                i += 1
            for key, value in eval(my_dict).items():
                setattr(obj, key, value)
            obj.save()
            return
        try:
            if str(int(args[3])) == args[3]:
                setattr(obj, args[2].replace("\"", ""), int(args[3]))
                obj.save()
                return
        except (ValueError, TypeError):
            try:
                if str(float(args[3])) == args[3]:
                    setattr(obj, args[2].replace("\"", ""), float(args[3]))
                    obj.save()
                    return
            except (ValueError, TypeError):
                """handling Double Quotes in arguments"""
                if args[3][0] == "\"":
                    value = ""
                    i = 3
                    while i < len(args):
                        value += args[i].replace("\"", "")
                        if i != len(args) - 1:
                            value += " "
                        i += 1
                    args[3] = value
                setattr(obj, args[2].replace("\"", ""), (args[3]))
                obj.save()

    def do_count(self, args):
        """`count` Usage count <class_name> or <class_name>.count()
        Example: count User or User.count()"""

        args = args.split(" ")
        if args == ['']:
            print("** class name missing **")
            return
        if args[0] not in self.__classes:
            print("** class doesn't exist **")
            return
        User_obj = 0
        Portfolio_obj = 0
        Music_obj = 0
        Movie_obj = 0
        Hobby_obj = 0
        Friend_obj = 0
        Book_obj = 0
        for i in dbstorage.all().values():
            if type(i) is User:
                User_obj += 1
            elif type(i) is Portfolio:
                Portfolio_obj += 1
            elif type(i) is Music:
                Music_obj += 1
            elif type(i) is Movie:
                Movie_obj += 1
            elif type(i) is Hobby:
                Hobby_obj += 1
            elif type(i) is Friend:
                Friend_obj += 1
            elif type(i) is Book:
                Book_obj += 1
        print(eval(args[0] + "_obj"))


if __name__ == '__main__':
    StoreCommand().cmdloop()
