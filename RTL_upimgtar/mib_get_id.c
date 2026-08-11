#include <stdio.h>

#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>

//  Hack to querry mibs by their numerical IDs, unless you have specific mib.h you cant get exact info what the number is...
//  Build:
//  /tmp/rsdk-1.5.10-4181-EB-2.6.30-0.9.30-m32u-130430/bin/rsdk-linux-gcc mib_get_id.c -ldl -o mib_get_id
//

typedef int (*add_func_t)(int id, void *value);

int main(int argc, char *argv[]) {
    int mibid = atoi(argv[1]);
    char username[128]={0};

    void* handle = dlopen("/lib/libmib.so", RTLD_LAZY);
    if (!handle) {
        fprintf(stderr, "Error opening library: %s\n", dlerror());
        return EXIT_FAILURE;
    }

    dlerror();

    add_func_t mib_get = (add_func_t)dlsym(handle, "mib_get");

    char* error = dlerror();
    if (error != NULL) {
        fprintf(stderr, "Error locating symbol: %s\n", error);
        dlclose(handle);
        return EXIT_FAILURE;
    }

    mib_get(mibid, username);
    printf("%d = \"%s\"\n", mibid , username);

    dlclose(handle);
    return EXIT_SUCCESS;
}





