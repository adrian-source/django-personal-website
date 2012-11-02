from django import template

#Django template custom math filters
#Ref : https://code.djangoproject.com/ticket/361
register = template.Library()

def mult(value, arg):
    "Multiplies the arg and the value"
    return int(value) * int(arg)

def sub(value, arg):
    "Subtracts the arg from the value"
    return int(value) - int(arg)

def div(value, arg):
    "Divides the value by the arg"
    return int(value) / int(arg)

register.filter('mult', mult)
register.filter('sub', sub)
register.filter('div', div)

def divwidth(value, arg):
	"value colswidth. arg numcols"
	return int(arg)*int(value)+(5*(int(value)-1))
register.filter('divwidth', divwidth)
