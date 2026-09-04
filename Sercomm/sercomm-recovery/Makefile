PROGS = sercomm-recovery
OBJS  = sercomm-recovery.o

INSTDIR   = $(prefix)/bin/
# Set SET-UID too
INSTMODE  = 4755
INSTOWNER = root
INSTGROUP = root

all: $(PROGS)

$(PROGS): $(OBJS)
	$(CC) $(LDFLAGS) $^ $(LDLIBS) -o $@

install:	$(PROGS)
	$(INSTALL) -d $(INSTDIR)
	$(INSTALL) -m $(INSTMODE) -o $(INSTOWNER) -g $(INSTGROUP) $(PROGS) $(INSTDIR)
	
clean:
	rm -f $(PROGS) *.o
