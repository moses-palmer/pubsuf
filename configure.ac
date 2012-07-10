AC_INIT([LibPubSuf], [1.0], [mosespalmer@gmail.com], [pubsuf])
AC_PREREQ([2.62])
AM_INIT_AUTOMAKE([1.10 -Wall -Werr])

## This library requires wget to build
AC_CHECK_PROG(WGET, [wget], [yes], [no])
if test "x$WGET" = "xno"; then
	AC_MSG_ERROR([This library requires wget to build])
fi

## Load packaged macros
AC_CONFIG_MACRO_DIR([m4])

## Add support for GObject introspection
GOBJECT_INTROSPECTION_CHECK([1.30.0])

## Add support for VAPI generation
VAPIGEN_CHECK()

## Add support for per-product flags
AM_PROG_CC_C_O

AC_CONFIG_HEADERS([config.h])
LT_INIT([disable-static])

# Define these substitions here to keep all version information in one place.
# For information on how to properly maintain the library version information,
# refer to the libtool manual, section "Updating library version information":
# http://www.gnu.org/software/libtool/manual/html_node/Updating-version-info.html
AC_SUBST([SO_VERSION], [0:0:0])
AC_SUBST([API_VERSION], [1.0])

# Override the template file name of the generated .pc file, so that there
# is no need to rename the template file when the API version changes.
AC_CONFIG_FILES([Makefile pubsuf-${API_VERSION}.pc:pubsuf.pc.in])
AC_OUTPUT
