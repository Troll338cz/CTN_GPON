#include <unistd.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/ioctl.h>
#include <stdbool.h>
#include <string.h>

#include <openssl/evp.h>

//	Build, libssl-dev needed:
//	gcc inna_adminpw.c -g -lcrypto -o innapw

//----- (0040B6F8) --------------------------------------------------------
void get_admin_password_16s(const char *input, size_t max_len)
{
    static const char alphabet[19] = "23456789abcdefghijk";
    static const char key[16]      = "iskrateliskratel";

    char buf[17] = {0};
    snprintf(buf, sizeof(buf), "%s", input);

    int B[16];
    int accum = 0;
    for (int i = 0; i < 16; ++i)
    {
        accum += (unsigned char)buf[15 - i] + (unsigned char)key[i];
        B[i] = accum;
    }

    char result_str[9];
    for (int k = 0; k < 8; ++k)
    {
        int val = B[k] + B[k + 8];
        int idx = val % 19;
        if (idx < 0) idx += 19;
        result_str[k] = alphabet[idx];
    }
    result_str[8] = '\0';

    char output[64];
    int result = snprintf(output, max_len, "%s", result_str);
    printf("get_admin_password_16s: %s\n", output);
}

//----- (0040B970) --------------------------------------------------------
void get_admin_password(uint64_t input, size_t a4)
{
    static const char charset[] = "iskratel23456789abcdefghijk";
    static const char *lookup = &charset[8];
    const size_t lookup_len = 19;

    uint32_t digits[32] = {0};
    int num_digits = 0;

    uint64_t temp = input;
    while (temp > 0) {
        digits[num_digits++] = (uint32_t)(temp % 10);
        temp /= 10;
    }

    uint32_t prefix_sums[32] = {0};
    if (num_digits > 0) {
        prefix_sums[0] = (uint32_t)charset[0] + digits[0];
        for (int j = 1; j < num_digits; ++j) {
            uint32_t char_val = (j < 8) ? (uint32_t)charset[j] : 32;
            prefix_sums[j] = prefix_sums[j - 1] + digits[j] + char_val;
        }
    }

    uint32_t work[8] = {0};
    int total_iterations = ((num_digits + 7) / 8) * 8;

    for (int k = 0; k < total_iterations; ++k) {
        uint32_t sum_val = (k < num_digits) ? prefix_sums[k] : prefix_sums[k % num_digits];
        work[k & 7] += sum_val;
    }

    char result[9];
    for (int i = 0; i < 8; ++i) {
        result[i] = lookup[work[i] % lookup_len];
    }
    result[8] = '\0';

    printf("get_admin_password: %s\n", result);
}

//----- (00425CA0) --------------------------------------------------------
void wifi_passwd_generator_16s(const char *input, int count)
{
    static const char charset1[] = "ABDEFGHAJK";
    static const char charset2[] = "23456789abdefghiajk";
    static const char key[]      = "rostelecomrostelecom";

    char formatted_input[17] = {0};
    if (input != NULL) {
        snprintf(formatted_input, sizeof(formatted_input), "%s", input);
    }

    int rev[16] = {0};
    for (int i = 0; i < 16; ++i) {
        rev[i] = (unsigned char)formatted_input[15 - i];
    }

    int cumulative_sum[16] = {0};
    int current_sum = 0;
    for (int i = 0; i < 16; ++i) {
        current_sum += rev[i] + (unsigned char)key[i];
        cumulative_sum[i] = current_sum;
    }

    char result[11] = {0};
    result[0] = charset1[cumulative_sum[0] % 10];
    for (int i = 1; i < 10; ++i) {
        result[i] = charset2[cumulative_sum[i] % 19];
    }

    printf("wifi_passwd_generator_16s: %s\n", result);
}

//----- (00425FA8) --------------------------------------------------------
void wifi_passwd_generator(const char *input_str, int max_len)
{
    static const char charset1[] = "rostelecom";
    static const char charset2[] = "ABDEFGHAJK";
    static const char charset3[] = "23456789abdefghiajk";

    long long val = atoll(input_str);
    int digits[10] = {0};
    int num_digits = 0;

    while (val > 0 && num_digits < 10) {
        digits[num_digits++] = (int)(val % 10);
        val /= 10;
    }

    if (num_digits == 0) {
        digits[0] = 0;
        num_digits = 1;
    }

    int target_len = 0;
    while (target_len < num_digits) {
        target_len += 10;
    }

    int prefix_sums[12] = {0};
    prefix_sums[0] = charset1[0] + digits[0];
    for (int j = 1; j < num_digits; j++) {
        char ch = (j < 10) ? charset1[j] : ' ';
        prefix_sums[j] = prefix_sums[j - 1] + digits[j] + ch;
    }

    int accumulated[10] = {0};
    for (int k = 0; k < target_len; k++) {
        accumulated[k % 10] += prefix_sums[k % num_digits];
    }

    char result[11];
    result[0] = charset2[accumulated[0] % 19];
    for (int i = 1; i < 10; i++) {
        result[i] = charset3[accumulated[i] % 19];
    }
    result[10] = '\0';

    int print_len = (max_len < 10) ? max_len : 10;
    if (print_len < 0) {
        print_len = 0;
    }

    printf("wifi_passwd_generator: %s\n", result);
}

// Rewriten, original version does stupid stuff hopefully right....
char *generate_ssl_passwd(int pwd_type, char *buff, const char* serialn, const char* magicval, size_t buff_size)
{
  char v12[256]; // [sp+E8h] [-108h] BYREF

  memset(v12, 0, sizeof(v12));

  EVP_MD_CTX *context = EVP_MD_CTX_new();
  const EVP_MD *md = EVP_sha256();
  unsigned char hash[EVP_MAX_MD_SIZE];
  unsigned int length_of_hash = 0;

  if (context == NULL) {
    fprintf(stderr, "Failed to create OpenSSL context.\n");
    return NULL;
  }

  if (EVP_DigestInit_ex(context, md, NULL) &&
    EVP_DigestUpdate(context, serialn, strlen(serialn)) &&
    EVP_DigestUpdate(context, magicval, strlen(magicval)) &&
    EVP_DigestFinal_ex(context, hash, &length_of_hash)) {
  }
  EVP_EncodeBlock(v12, hash, length_of_hash);
  EVP_MD_CTX_free(context);


  return strncpy(buff, v12, buff_size);
}

//----- (0040F7A4) --------------------------------------------------------
char *admin_passwd_generator_other(char *buff, const char *serial, size_t buff_size)
{
  char ssl_out[32]; // [sp+30h] [-20h] BYREF

  generate_ssl_passwd(1, ssl_out, serial, "Iskrateliadmin", 32u);
  return strncpy(buff, ssl_out, buff_size);
}

//----- (0040F7A4) --------------------------------------------------------
char *wifi_passwd_generator_other(char *buff, const char *serial, size_t buff_size)
{
  char ssl_out[32]; // [sp+30h] [-20h] BYREF

  generate_ssl_passwd(1, ssl_out, serial, "Iskratelwifi", 32u);
  return strncpy(buff, ssl_out, buff_size);
}

/*

Full code in fad.c
int change_login_passwd_and_ssid()

  cfg_getstr(v42, 32, "/runtime/nvram/serial");
  cfg_getstr(v41, 32, "/runtime/nvram/serial_gpon");

  if ( fad_get_customize() == 6 ) // == "T2"
    v0 = "/runtime/layout/1stwanmac";
  else
    v0 = "/runtime/layout/lanmac";
  cfg_getstr(v43, 32, v0);
  mac_num = get_mac_num(v43, 4);
  v5 = get_mac_num(v43, 5);
  v7 = get_mac_num(v43, 6);

// SSID Generation

LABEL_66:
              snprintf(v48, 0x80u, "Innbox-internet-%02x%02x%02x-Guest%d", mac_num, v5, v7, v2);
              goto LABEL_197;
            }
LABEL_190:
            snprintf(v48, 0x80u, "Innbox-internet-%02x%02x%02x", mac_num, v5, v7);
            goto LABEL_197;
          }
LABEL_192:
          snprintf(v48, 0x80u, "Innbox-internet-%02x%02x%02x-Guest%d", mac_num, v5, v7, v6);
          goto LABEL_197;
        }


// Password generation
    if ( !strcmp(v47, "##########") ) - SSID Not disabled
      fad_setstr_wo_et((int)v48, (const char *)(v51 - 17860), v8);
    if ( fad_get_customize() == 2 ) // == "Rostelecom"
    {
      memset(v48, 0, 0x80u);
      v12 = strlen(v42);
      if ( v12 == 10 )
      {
        v13 = 10;
LABEL_217:
        wifi_passwd_generator(v48, v42, v13);
        goto LABEL_225;
      }
      v14 = 10;
LABEL_219:
      if ( v12 == 16 )
        wifi_passwd_generator_16s(v48, v42, v14);
      else
        wifi_passwd_generator_other(v48, (int)v42, v14);
      goto LABEL_225;
    }
    if ( fad_get_customize() == 10 ) //  == "Optima"
    {
      if ( v42[0] )
        snprintf(v48, 0x80u, "OPTIMA%s", v42);
      else
        snprintf(v48, 0x80u, "OPTIMA%02X%02X%02X", mac_num, v5, v7);
      goto LABEL_225;
    }
    if ( fad_get_customize() != 6 ) != "T2"
    {
      if ( fad_get_customize() == 13 || fad_get_customize() == 18 ) // == "Ozone" or == "Vitis"
      {
        if ( v42[0] )
          snprintf(v48, 0x80u, "%s", v42);
        else
          snprintf(v48, 0x80u, "%02X%02X%02X", mac_num, v5, v7);
        goto LABEL_225;
      }
      if ( fad_get_customize() != 19 && fad_get_customize() == 27 ) // != "Zeop" and == "MGTS"
      {
        memset(v48, 0, 0x80u);
        v12 = strlen(v42);
        if ( v12 == 10 )
        {
          v13 = 8;
          goto LABEL_217;
        }
        v14 = 8;
        goto LABEL_219;
      }
    }

    if ( v42[0] )
      snprintf(v48, 0x80u, "INNBOX%s", v42);
    else
      snprintf(v48, 0x80u, "INNBOX%02X%02X%02X", mac_num, v5, v7);


    cfg_setstr(v48, "/runtime/wps/inf:%d/default_password", v8);
    cfg_getstr(v46, 128, "/InternetGatewayDevice/LANDevice:1/WLANConfiguration:%d/PreSharedKey:1/KeyPassphrase", v8);
*/


int main(int argc, char *argv[]) {
        // Other samples found
        // 13 - WiFi pw == SN
        // 10 - %s%s "ISP Name from SSID allcaps" or "INNBOX", SN
        // "Ozone" or == "Vitis" - 10 WiFi pw == SN

        const char* a;
        puts("-------------------------------------");
        // SN type 10 char:
        // Matches with Innbox_SN10.png
        a = "3115002624";
        uint64_t v16;
        v16 = strtoull(a, 0, 10);
        get_admin_password(v16, 9u);
        wifi_passwd_generator(a, 10); // MTS Innbox G84, len = 8

        puts("-------------------------------------");

        // SN type 16 char:
        // Untested, couldn't find example
        a = "1234567890123456";
        get_admin_password_16s(a,9u);
        wifi_passwd_generator_16s(a, 10);
        puts("-------------------------------------");
        // Untested:
        char b[64];
        memset(b, 0, sizeof(b));
        // cfg_getstr(v40, 32, "/InternetGatewayDevice/DeviceInfo/Manufacturer"); == &g_env_manu -- See customerid.py to find your value
        const char* v40 = "Iskratel";
        printf( "admin_passwd_generator_other: %s\n", admin_passwd_generator_other(b, a, 8u));
        printf( "wifi_passwd_generator_other: %s\n", wifi_passwd_generator_other(b, a, 10));
        printf( "generate_ssl_passwd: %s\n", generate_ssl_passwd(1, b, a, v40, 0x10u));
        puts("-------------------------------------");
}
