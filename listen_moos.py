from listen import listen
import settings


def main():
    listen(
        settings.MOOS_OUTPUT_DIR,
        settings.INPUT_RAW_SCAN_CHANNEL,
        "MERNOS_MOOS")


if __name__ == "__main__":
    main()
