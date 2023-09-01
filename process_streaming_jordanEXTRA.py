"""

Streaming Process: Uses port 9999

Create a fake stream of data. 
Use temperature data from the batch process.

Reverse the order of the rows to read OLDEST data first.

Important! 

We'll stream forever - or until we read the end of the file. 
Use use Ctrl-C to stop. (Hit Control key and c key at the same time.)

Explore more at 
https://wiki.python.org/moin/UdpCommunication

"""

# Import from Python Standard Library

import csv
import socket
import time
import logging

# Set up basic configuration for logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# Declare program constants (typically constants are named with ALL_CAPS)

HOST = "localhost"
PORT = 9999
ADDRESS_TUPLE = (HOST, PORT)
INPUT_FILE_NAME = "orders_deliveries.csv"
OUTPUT_FILE_NAME = "outEXTRA.txt"

# Define program functions (bits of reusable code)


def prepare_message_from_row(row):
    """Prepare a binary message from a given row."""
    Country, Customer_Name, Delivery_Year, Engine, Model_Series, Order_Month, Order_Year, Region, Delivery_Total, Order_Total, Unfilled_Orders = row
    # use an fstring to create a message from our data
    # notice the f before the opening quote for our string?
    fstring_message = f"[{Country}, {Customer_Name}, {Delivery_Year}, {Engine}, {Model_Series}, {Order_Month}, {Order_Year}, {Region}, {Delivery_Total}, {Order_Total}, {Unfilled_Orders}]"

    # prepare a binary (1s and 0s) message to stream
    MESSAGE = fstring_message.encode()
    logging.debug(f"Prepared message: {fstring_message}")
    return MESSAGE



def stream_row(input_file_name, address_tuple, OUTPUT_FILE_NAME):
    """Read from input file and stream data."""
    logging.info(f"Starting to stream data from {input_file_name} to {address_tuple}.")

    # Open the input file for reading and the output file for writing
    with open(input_file_name, "r") as input_file, open(OUTPUT_FILE_NAME, "w") as output_file:
        logging.info(f"Opened for reading: {input_file_name}.")
        output_file.write("===============================================\n")
        output_file.write("Starting fake streaming process.\n")
        output_file.write("===============================================\n")

        # Create a reader object from our input file
        reader = csv.reader(input_file, delimiter=",")

        header = next(reader)  # Skip header row
        logging.info(f"Skipped header row: {header}")
        output_file.write(f"Skipped header row: {header}\n")

        # Create a socket object
        ADDRESS_FAMILY = socket.AF_INET
        SOCKET_TYPE = socket.SOCK_DGRAM

        sock_object = socket.socket(ADDRESS_FAMILY, SOCKET_TYPE)

        # Read each row of the input file and stream it
        for row in reader:
            MESSAGE = prepare_message_from_row(row)
            sock_object.sendto(MESSAGE, address_tuple)
            log_message = f"Sent: {MESSAGE} on port {PORT}. Hit CTRL-c to stop."
            logging.info(log_message)
            output_file.write(f"{log_message}\n")
            time.sleep(3)

        # Close the socket object
        output_file.write("Streaming complete!\n")
        output_file.write("===============================================\n")

# ---------------------------------------------------------------------------
# If this is the script we are running, then call some functions and execute code!
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        logging.info("===============================================")
        logging.info("Starting fake streaming process.")
        stream_row(INPUT_FILE_NAME, ADDRESS_TUPLE, OUTPUT_FILE_NAME)
        logging.info("Streaming complete!")
        logging.info("===============================================")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

