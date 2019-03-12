from listen import listen
import settings


def main():
    listen(
        settings.GPU_OUTPUT_DIR,
        settings.OUTPUT_RAW_SCAN_CHANNEL,
        "MERNOS_GPU")


if __name__ == "__main__":
    main()
