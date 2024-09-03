// Megasquirt ms3 can emulator with CAN-BUS Shield, send data

#include <SPI.h>
#define CAN_2515
#include "Nextion.h"
#include <SoftwareSerial.h> //Include the library

SoftwareSerial NextionSerial(10, 11); // RX, TX


// Set SPI CS Pin according to your hardware

#if defined(SEEED_WIO_TERMINAL) && defined(CAN_2518FD)
// For Wio Terminal w/ MCP2518FD RPi Hat：
// Channel 0 SPI_CS Pin: BCM 8
// Channel 1 SPI_CS Pin: BCM 7
// Interupt Pin: BCM25
const int SPI_CS_PIN  = BCM8;
const int CAN_INT_PIN = BCM25;
#else

// For Arduino MCP2515 Hat:
// the cs pin of the version after v1.1 is default to D9
// v0.9b and v1.0 is default D10
const int SPI_CS_PIN = 9;
const int CAN_INT_PIN = 2;
#endif


#ifdef CAN_2518FD
#include "mcp2518fd_can.h"
mcp2518fd CAN(SPI_CS_PIN); // Set CS pin
#endif

#ifdef CAN_2515
#include "mcp2515_can.h"
mcp2515_can CAN(SPI_CS_PIN); // Set CS pin
#endif

void setup() {
    SERIAL_PORT_MONITOR.begin(115200);
    while(!Serial){};
    NextionSerial.begin(9600);

    while (CAN_OK != CAN.begin(CAN_500KBPS)) {             // init can bus : baudrate = 500k
        SERIAL_PORT_MONITOR.println("CAN init fail, retry...");
        delay(100);
    }
    SERIAL_PORT_MONITOR.println("CAN init ok!");
}

//unsigned char stmp[8] = {0xFF, 0x01, 0x10, 0x0A, 0x00, 0x00, 0x00, 0x00};
unsigned char buf[8] = {0, 1, 2, 3, 4, 5, 6, 7};
int short canMsg = 255;
int short canMsg2[2] = {0xFF, 0x01};
//uint8_t const msg_data[] = {0xCA,0xFE,0,0,0,0,0,0}; this works
uint8_t const stmp[] = {0xFE,7,6,5,4,3,2,1};
unsigned char tps[8] = {0.0, 1.0, 2.0, 100.0, 3, 2, 1, 0};
unsigned char oil_p[8] = {20.0, 100, 2.0, 100.0, 3, 2, 1, 0};
unsigned char afr[8] = {500.0, 115.0, 130.0, 140.0, 7000, 8000, 9000, 6000};
unsigned char bat[8] = {134, 115, 130.0, 140.0, 7000, 8000, 9000, 6000};
unsigned char rpm[8] = {3000, 3200, 3400, 3500, 7000, 8000, 9000, 6000};



void loop() {
    // send data:  id = 0x00, standrad frame, data len = 8, stmp: data buf
    afr[1] = random(110,140);
    bat[0] = random(120,140);
    oil_p[0] = random(15,50);
    oil_p[4] = random(15,50);




//void loop() {
//    CAN.sendMsgBuf(1512, 0, 2, 2, 2, canMsg2);
//    CAN.sendMsgBuf(1512, 0, 8, tps);
    CAN.sendMsgBuf(1513, 0, 8, oil_p);
    CAN.sendMsgBuf(1515, 0, 8, bat);
    CAN.sendMsgBuf(1514, 0, 8, afr);
    
    delay(100);                       // send data every 1s
    SERIAL_PORT_MONITOR.println("CAN BUS sendMsgBuf ok!");
}

// END FILE
