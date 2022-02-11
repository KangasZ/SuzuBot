# This is SuzuBot
## Please be kind.

# Requirements:
* Discord.py ver 1.7.3
### Make a config.json:
```json
{
  "token" : "yourtokenhere",
  "prefix" : "yourprefixhere",
  "owner" : 99999999999
}
```
```
venv/bin/activate
screen -S discord
Ctrl+a d
```
# Commands
## Clown 9 : C9
### [prefix]c9 [arg]
#### arg
- perkz
- worlds
- win
- clown

## OWNER ONLY: Rules : rules
### [prefix]rules [arg]
#### arg
##### list
Lists all rules
##### dev
### [prefix]rules [name] [command] [args]*
#### name
- name of your command
#### command
##### create [title] [color]
Needs to be executed first
- Title: "string here"
- Color: INTEGER
##### field [name] [values]
Adds field
- Name: "name of field here"
- Values: "values for field here"
##### footer [value]
Adds a footer
- Values: "values for field here"
##### clear
Clears all fields and footer
##### post
posts current name into current channel. Uses roles
##### preview
posts current name into current channel. Does not use roles