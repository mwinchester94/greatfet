/*
 * Copyright 2016 Dominic Spill
 * Copyright 2016 Schuyler St. Leger
 *
 * This file is part of GreatFET.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2, or (at your option)
 * any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#include "usb_api_adc.h"
#include "usb.h"
#include "usb_queue.h"
#include "usb_endpoint.h"
#include "usb_bulk_buffer.h"

#include <stddef.h>
#include <greatfet_core.h>
#include <libopencm3/lpc43xx/adc.h>
// #include <libopencm3/lpc43xx/m4/nvic.h>
// #include <libopencm3/cm3/vector.h>

volatile bool adc_mode_enabled = false;

usb_request_status_t usb_vendor_request_adc_init(
		usb_endpoint_t* const endpoint, const usb_transfer_stage_t stage) {
	usb_endpoint_init(&usb0_endpoint_bulk_in);
	if (stage == USB_TRANSFER_STAGE_SETUP) {
		adc_mode_enabled = true;
		usb_transfer_schedule_ack(endpoint->in);
	}
	return USB_REQUEST_STATUS_OK;
}

usb_request_status_t usb_vendor_request_read_adc(
		usb_endpoint_t* const endpoint, const usb_transfer_stage_t stage) {
	if (stage == USB_TRANSFER_STAGE_SETUP) {
		usb_transfer_schedule_ack(endpoint->in);
	}
	return USB_REQUEST_STATUS_OK;
}




#define BLK_LEN 0x4000

static uint8_t tx_buffer[] = "hello, there...";
static uint8_t tx_pos = 0;

void tx_complete(void* buffer, unsigned int transferred) {
	(void)buffer;
	tx_pos += transferred;
}

void adc_mode(void) {
	static bool first = true;
	if (first) {
		usb_endpoint_init(&usb0_endpoint_bulk_in);
		first = false;
	}

	usb_transfer_schedule_block(
			&usb0_endpoint_bulk_in, /* endpoint */
			&tx_buffer[tx_pos], 		/* data */
			(tx_pos < 15 ? 1 : 0), 											/* maximum_length */
			&tx_complete, 							/* completion_cb */
			0); 										/* user_data */
}
