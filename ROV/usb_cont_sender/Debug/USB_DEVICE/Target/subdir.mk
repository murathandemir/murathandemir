################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (10.3-2021.10)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../USB_DEVICE/Target/usbd_conf.c 

OBJS += \
./USB_DEVICE/Target/usbd_conf.o 

C_DEPS += \
./USB_DEVICE/Target/usbd_conf.d 


# Each subdirectory must supply rules for building sources it contributes
USB_DEVICE/Target/%.o USB_DEVICE/Target/%.su: ../USB_DEVICE/Target/%.c USB_DEVICE/Target/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m3 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F103xB -c -I../Core/Inc -I/home/murathan/STM32Cube/Repository/STM32Cube_FW_F1_V1.8.4/Drivers/STM32F1xx_HAL_Driver/Inc/Legacy -I/home/murathan/STM32Cube/Repository/STM32Cube_FW_F1_V1.8.4/Drivers/STM32F1xx_HAL_Driver/Inc -I/home/murathan/STM32Cube/Repository/STM32Cube_FW_F1_V1.8.4/Drivers/CMSIS/Device/ST/STM32F1xx/Include -I/home/murathan/STM32Cube/Repository/STM32Cube_FW_F1_V1.8.4/Drivers/CMSIS/Include -I../USB_DEVICE/App -I../USB_DEVICE/Target -I/home/murathan/STM32Cube/Repository/STM32Cube_FW_F1_V1.8.4/Middlewares/ST/STM32_USB_Device_Library/Core/Inc -I/home/murathan/STM32Cube/Repository/STM32Cube_FW_F1_V1.8.4/Middlewares/ST/STM32_USB_Device_Library/Class/CDC/Inc -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"

clean: clean-USB_DEVICE-2f-Target

clean-USB_DEVICE-2f-Target:
	-$(RM) ./USB_DEVICE/Target/usbd_conf.d ./USB_DEVICE/Target/usbd_conf.o ./USB_DEVICE/Target/usbd_conf.su

.PHONY: clean-USB_DEVICE-2f-Target

