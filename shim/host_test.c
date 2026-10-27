/* Render the console layout on the host: ./out/host_test && view out/host.ppm */
#include <stdio.h>
#include "console.h"

static uint32_t host_fb[FB_H * FB_STRIDE / 4];

int main(void)
{
	con_fb = host_fb;
	con_clear(RED);
	con_str("SHIM", "flame (SM4450) milestone 4: xnu loader");
	con_str("MODEL", "Xiaomi Redmi 14R 5G (flame)");
	con_str("SOC", "Qualcomm SM4450 (ravelin)");
	con_hex2("GICv3", "gicd=", 0x17200000, "gicr=", 0x17260000);
	con_hex2("FB", "w=", FB_W, "h=", FB_H);
	con_hex2("PSCI", "ver=", 0x10001, "smccc=", 0x10002);
	con_hex2("CPU7", "ret=", 0, "mpidr=", 0x81000700);
	FILE *f = fopen("out/host.ppm", "wb");
	fprintf(f, "P6 %d %d 255\n", FB_W, FB_H);
	for (int i = 0; i < FB_W * FB_H; i++) {
		unsigned char px[3] = { host_fb[i] >> 16, host_fb[i] >> 8, host_fb[i] };
		fwrite(px, 1, 3, f);
	}
	fclose(f);
	return 0;
}
