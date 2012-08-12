## Make sure the generated PC files are available without installation.
export PKG_CONFIG_PATH=.


## Place generated object files (.o) into the same directory as their source
## files, in order to avoid collisions when non-recursive make is used.
AUTOMAKE_OPTIONS = subdir-objects


## Additional flags to pass to aclocal when it is invoked automatically at
## make time. The ${ACLOCAL_FLAGS} variable is picked up from the environment
## to provide a way for the user to supply additional arguments.
ACLOCAL_AMFLAGS = ${ACLOCAL_FLAGS} -I m4


## Enable GObject introspection
DISTCHECK_CONFIGURE_FLAGS = --enable-introspection
EXTRA_DIST = m4/introspection.m4 m4/vapigen.m4


## Define a libtool archive target "libexample-@API_VERSION@.la", with
## @API_VERSION@ substituted into the generated Makefile at configure time.
##
## The libtool archive file (.la) will be installed into the directory named
## by the predefined variable $(bindir), along with the actual shared library
## file (.so).
lib_LTLIBRARIES = libpubsuf-@API_VERSION@.la


## This library depends on generated data.
##
## tools/effective_tld_names.dat is the list of effective TLD names from
## Mozilla.
##
## tools/test.txt is the list of tests.
BUILT_SOURCES = \
	tools/effective_tld_names.dat \
	pubsuf/etlds.c \
	tools/test.txt \
	tests/etld-tests.def
CLEANFILES = \
	tools/effective_tld_names.dat \
	pubsuf/etlds.c \
	tools/test.txt \
	tests/etld-tests.def

## Download the effective TLDs from Mozilla.
tools/effective_tld_names.dat:
	sh tools/effective_tld_names.sh

## Convert the effective TLD names list to C source.
pubsuf/etlds.c: tools/effective_tld_names.dat
	python tools/etld-parser.py \
		--c-source-c "pubsuf/etlds.c" \
		c-source \
		"tools/effective_tld_names.dat"

## Download the test definitions from Mozilla.
tools/test.txt:
	sh tools/test.sh

## Convert the test text file to a test definition file.
tests/etld-tests.def: tools/test.txt
	python tools/test-parser.py \
		"tools/test.txt" \
		"tests/etld-tests.def"


## Define the source file list for the "libpubsuf-@API_VERSION@.la" target.
## Note that @API_VERSION@ is not interpreted by Automake and will therefore be
## treated as if it were literally part of the target name, and the variable
## name derived from that.
libpubsuf_@API_VERSION@_la_SOURCES = \
	pubsuf/etlds.c \
	pubsuf/public-suffix.c


## Instruct libtool to include ABI version information in the generated shared
## library file (.so). The library ABI version is defined in configure.ac, so
## that all version information is kept in one place.
libpubsuf_@API_VERSION@_la_LDFLAGS = -version-info $(SO_VERSION)


## Define the list of public header files and their install location. The
## nobase_ prefix instructs Automake to not strip the directory part from each
## filename, in order to avoid the need to define separate file lists for each
## installation directory. This only works if the directory hierarchy in the
## source tree matches the hierarchy at the install location, however.
pubsuf_includedir = $(includedir)/pubsuf-$(API_VERSION)
nobase_pubsuf_include_HEADERS = \
	pubsuf.h \
	pubsuf/public-suffix.h


## Install the generated pkg-config file (.pc) into the expected location for
## architecture-dependent package configuration information. Occasionally,
## pkg-config files are also used for architecture-independent data packages,
## in which case the correct install location would be $(datadir)/pkgconfig.
pkgconfigdir = $(libdir)/pkgconfig
pkgconfig_DATA = pubsuf-$(API_VERSION).pc

## Install the static PC file if requested
if STATIC_INSTALLATION
pkgconfig_DATA += pubsuf-static-$(API_VERSION).pc
endif


## Generate GObject Introspection data.
-include $(INTROSPECTION_MAKEFILE)
INTROSPECTION_GIRS =

if HAVE_INTROSPECTION
introspection_sources = $(nobase_pubsuf_include_HEADERS)

PublicSuffix-@API_VERSION@.gir: libpubsuf-@API_VERSION@.la
PublicSuffix_1_0_gir_INCLUDES = GObject-2.0
PublicSuffix_1_0_gir_CFLAGS = $(INCLUDES)
PublicSuffix_1_0_gir_LIBS = libpubsuf-@API_VERSION@.la
PublicSuffix_1_0_gir_FILES = $(introspection_sources)
PublicSuffix_1_0_gir_NAMESPACE = PublicSuffix
PublicSuffix_1_0_gir_PACKAGES = pubsuf-$(API_VERSION)
PublicSuffix_1_0_gir_VERSION = @API_VERSION@
PublicSuffix_1_0_gir_SCANNERFLAGS = --header-only --c-include=pubsuf.h
INTROSPECTION_GIRS += PublicSuffix-@API_VERSION@.gir

girdir = $(datadir)/gir-1.0
gir_DATA = $(INTROSPECTION_GIRS)

typelibdir = $(libdir)/girepository-1.0
typelib_DATA = $(INTROSPECTION_GIRS:.gir=.typelib)

CLEANFILES += $(gir_DATA) $(typelib_DATA)
endif

## Generate a VAPI file from the GObject introspection data
-include $(VAPIGEN_MAKEFILE)
VAPIGEN_VAPIS =

if ENABLE_VAPIGEN
pubsuf-@API_VERSION@.vapi: $(INTROSPECTION_GIRS)
pubsuf_1_0_vapi_METADATADIRS = $(srcdir)
pubsuf_1_0_vapi_FILES = $(INTROSPECTION_GIRS)
VAPIGEN_VAPIS += pubsuf-@API_VERSION@.vapi

vapidir = $(VAPIGEN_VAPIDIR)
vapi_DATA = $(VAPIGEN_VAPIS)

CLEANFILES += VAPIGEN_VAPIS
endif


## Define an independent executable script for inclusion in the distribution
## archive. However, it will not be installed on an end user's system due to
## the noinst_ prefix.
dist_noinst_SCRIPTS = autogen.sh


## Build a test program, but do not install it
check_PROGRAMS = pubsuftest

## Simply compile all source files when building the test program
pubsuftest_SOURCES = \
	tests/test/test-main.c

## Make sure the test program depends on all test definition files
EXTRA_pubsuftest_DEPENDENCIES = \
	tests/tests.def \
	tests/etld-tests.def

## Link the test program
pubsuftest_LDFLAGS = -l:.libs/libpubsuf-$(API_VERSION).so

## Run pubsuftest as part of the test suite
TESTS = pubsuftest
TESTS_ENVIRONMENT = LD_LIBRARY_PATH=.libs
