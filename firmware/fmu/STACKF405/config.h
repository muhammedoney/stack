/*
 * This file is part of Betaflight.
 *
 * Betaflight is free software. You can redistribute this software
 * and/or modify this software under the terms of the GNU General
 * Public License as published by the Free Software Foundation,
 * either version 3 of the License, or (at your option) any later
 * version.
 *
 * Betaflight is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 *
 * See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public
 * License along with this software.
 *
 * If not, see <http://www.gnu.org/licenses/>.
 */

/*
 * Stack FMU (M1, F405) — Betaflight kart tanımı TASLAĞI (gomulu-yazilim, 2026-11-12)
 *
 * Taban: betaflight/config configs/SPBE/SPEEDYBEEF405V4/config.h
 *        (betaflight/config @ cacb3a06d7d9, GPL-3.0). Pin/zamanlayıcı/DMA tek kaynak:
 *        docs/pin-haritasi.md §1 (v0.1). Farklar yalnız §1.4'tekiler.
 * Yazılım: Betaflight >= 2025.12 (APM32F405 platformu 2025.12'de geldi); 2026.6.2'de
 *        kaynak kodundan kontrol edildi. DERLEYİCİDE DOĞRULANACAK (arm-none-eabi-gcc yok).
 *
 * MCU: Seri üretim APM32F405RGT6 (KRR-010). STM32F405RGT6 ALT dizilirse aynı dosya
 *      ikinci bir klasörde (öneri: STACKF405_STM) yalnız FC_TARGET_MCU satırı
 *      "STM32F405" yapılarak derlenir. Betaflight bir config'e tek MCU bağlar → iki imaj
 *      (docs/rapor/yazilim-inceleme.md §1).
 */

#pragma once

#define FC_TARGET_MCU     APM32F405     // STM32 ALT varyantında: STM32F405

#define BOARD_NAME        STACKF405
#define MANUFACTURER_ID   STCK          // GEÇİCİ: Betaflight Manufacturers.md kaydı gerekir

// --- Sensörler (muadiller aynı imajda otomatik tanınır, SYS-095 d) ---
#define USE_ACC
#define USE_GYRO
#define USE_GYRO_SPI_ICM42688P          // TDK ICM-42688-P, WHO_AM_I 0x47
#define USE_ACC_SPI_ICM42688P
#define USE_GYRO_SPI_ICM42605           // TDK ICM-42605 (0x42) — ALT adayı
#define USE_ACC_SPI_ICM42605
#define USE_ACCGYRO_IIM42652            // TDK IIM-42652 (0x6F) — ALT adayı
#define USE_ACCGYRO_ICM42686P           // TDK ICM-42686-P (0x44) — yalnız BF (AP'de yok)

#define USE_BARO
#define USE_BARO_DPS310                 // ID 0x10 (Infineon DPS310/DPS368) ve 0x11 (SPA06-003, SPL07-003, Tokmas "DPS368")
#define USE_BARO_SPA06_003              // 2026.6+: 0x11 "SPA06_003" diye raporlanır; eski sürümde etkisiz

#define USE_FLASH
#define USE_FLASH_M25P16                // SPI NOR JEDEC tablosu (W25Q128JV 0xEF4018/0xEF7018 ...)
#define USE_FLASH_W25Q128FV             // SPI'da M25P16'yı çağırır (common_post.h); SPEEDYBEE/MAMBA ile aynı alışkanlık

#define USE_MAX7456                     // AT7456E / MAX7456 (tip otomatik algılanır)

// --- Pinler (docs/pin-haritasi.md §1.1) ---
#define BEEPER_PIN           PC15
#define MOTOR1_PIN           PB6
#define MOTOR2_PIN           PB7
#define MOTOR3_PIN           PB0
#define MOTOR4_PIN           PB1
#define MOTOR5_PIN           PC8
#define MOTOR6_PIN           PC9
#define MOTOR7_PIN           PB10
#define MOTOR8_PIN           PA15
#define RX_PPM_PIN           PA3
#define SERVO1_PIN           PB15        // S9 pedi
#define LED_STRIP_PIN        PA8
#define UART1_TX_PIN         PA9         // DJI / MSP
#define UART2_TX_PIN         PA2         // alıcı
#define UART3_TX_PIN         PC10
#define UART4_TX_PIN         PA0         // analog VTX SmartAudio/Tramp
#define UART5_TX_PIN         PC12        // fark #2: SpeedyBee V4'te yok
#define UART6_TX_PIN         PC6         // GPS
#define UART1_RX_PIN         PA10
#define UART2_RX_PIN         PA3
#define UART3_RX_PIN         PC11
#define UART4_RX_PIN         PA1
#define UART5_RX_PIN         PD2
#define UART6_RX_PIN         PC7
#define I2C1_SCL_PIN         PB8
#define I2C1_SDA_PIN         PB9
#define LED0_PIN             PC13
#define SPI1_SCK_PIN         PA5
#define SPI2_SCK_PIN         PB13
#define SPI3_SCK_PIN         PB3
#define SPI1_SDI_PIN         PA6
#define SPI2_SDI_PIN         PC2
#define SPI3_SDI_PIN         PB4
#define SPI1_SDO_PIN         PA7
#define SPI2_SDO_PIN         PC3
#define SPI3_SDO_PIN         PB5
#define CAMERA_CONTROL_PIN   PB14
#define ADC_VBAT_PIN         PC0
#define ADC_RSSI_PIN         PC5         // fark #4: ESC2 akımı (ArduPilot BATT2); BF'de RSSI
#define ADC_CURR_PIN         PC1
#define FLASH_CS_PIN         PC14        // fark #1: SpeedyBee'de SD kart CS
#define PINIO1_PIN           PB11        // 9 V BEC EN (U102 SY8303)
#define MAX7456_SPI_CS_PIN   PB12
#define GYRO_1_EXTI_PIN      PC4
#define GYRO_1_CS_PIN        PA4

// TIMER_PIN_MAP(indeks, pin, sıra(occurrence), dmaopt) — SpeedyBee V4 ile aynı.
// Sıra/DMA, timer_apm32f4xx.c ve dma_reqmap_mcu.c (APM32) ile STM32 tablolarının
// birebir aynı olduğu kaynaktan doğrulandı (rapor §1.4).
#define TIMER_PIN_MAPPING \
    TIMER_PIN_MAP( 0, PB6,  1,  0) /* M1 TIM4_CH1  DMA1 S0 ch2 */ \
    TIMER_PIN_MAP( 1, PB7,  1,  0) /* M2 TIM4_CH2  DMA1 S3 ch2 */ \
    TIMER_PIN_MAP( 2, PB0,  2,  0) /* M3 TIM3_CH3  DMA1 S7 ch5 */ \
    TIMER_PIN_MAP( 3, PB1,  2,  0) /* M4 TIM3_CH4  DMA1 S2 ch5 */ \
    TIMER_PIN_MAP( 4, PC8,  2,  0) /* M5 TIM8_CH3  DMA2 S2 ch0 (dmaopt 1 = S4 KULLANMA: ADC1) */ \
    TIMER_PIN_MAP( 5, PC9,  2,  0) /* M6 TIM8_CH4  DMA2 S7 ch7 */ \
    TIMER_PIN_MAP( 6, PB10, 1,  0) /* M7 TIM2_CH3  DMA1 S1 ch3 */ \
    TIMER_PIN_MAP( 7, PA15, 1,  0) /* M8 TIM2_CH1  DMA1 S5 ch3 */ \
    TIMER_PIN_MAP( 8, PB15, 3, -1) /* servo TIM12_CH2, DMA yok */ \
    TIMER_PIN_MAP( 9, PB14, 3, -1) /* CC TIM12_CH1, DMA yok */ \
    TIMER_PIN_MAP(10, PA8,  1,  0) /* LED TIM1_CH1 DMA2 S6 ch0 */ \
    TIMER_PIN_MAP(11, PA3,  3, -1) /* PPM TIM9_CH2, DMA yok */

#define ADC1_DMA_OPT 1                   // fark #3: DMA2 S4 → SPI1 (gyro) DMA2 S0/S3'ü alır

#define MAG_I2C_INSTANCE     I2CDEV_1
#define BARO_I2C_INSTANCE    I2CDEV_1     // adres 0x76 sürücü varsayılanı (SDO → GND)
#define FLASH_SPI_INSTANCE   SPI3
#define MAX7456_SPI_INSTANCE SPI2
#define GYRO_1_SPI_INSTANCE  SPI1
#define GYRO_1_ALIGN         CW0_DEG      // YER TUTUCU: IMU yerleşimi belli olunca (pcb-muhendisi)

#define DEFAULT_BLACKBOX_DEVICE      BLACKBOX_DEVICE_FLASH
#define DEFAULT_DSHOT_BURST          DSHOT_DMAR_OFF
#define DEFAULT_DSHOT_BITBANG        DSHOT_BITBANG_OFF   // bit-bang TIM1/TIM8 ister, LED şeridiyle çakışır
#define DEFAULT_CURRENT_METER_SOURCE CURRENT_METER_ADC
#define DEFAULT_VOLTAGE_METER_SOURCE VOLTAGE_METER_ADC
#define DEFAULT_VOLTAGE_METER_SCALE  150   // fark #6: 140 k / 10 k = 15:1
#define DEFAULT_CURRENT_METER_SCALE  100   // RSA240C / INA240A3 ×100, 0.1 mΩ → 10 mV/A (birim mV/10A). SJ101 kapalıysa (iki ESC ortalaması) 50
#define DEFAULT_CURRENT_METER_OFFSET 0     // REF1 = REF2 = GND, tek yönlü
#define BEEPER_INVERTED
#define SYSTEM_HSE_MHZ 8

// 9 V BEC: 129 = 0x81 = OUT_PP | INVERTED → açılışta PB11 HIGH → 9 V AÇIK.
// PINIO1_BOX 40 = USER1: USER1 anahtarı aktifken 9 V KAPANIR. SpeedyBee V4'teki 0 (= ARM)
// KOPYALANMAZ: bizim donanımda (EN yüksekte açık) silahlanınca 9 V'u keserdi.
#define PINIO1_CONFIG 129
#define PINIO1_BOX    40

#define SERIALRX_UART SERIAL_PORT_USART2
#define MSP_UART      SERIAL_PORT_USART1
// ESC_SENSOR_UART tanımlanmadı: Bluejay seri telemetri vermez (çift yönlü DShot EDT kullanılır)
