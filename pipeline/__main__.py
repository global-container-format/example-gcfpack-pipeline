from .framework import execute_pipeline

from .stages import (
    create_temporary_folder,
    create_image_data,
    create_gcf_description,
    pack_gcf_file,
    print_results,
    wait_for_user_input
)


def main():
    stages = (
        create_temporary_folder,
        create_image_data,
        create_gcf_description,
        pack_gcf_file,
        print_results,
        wait_for_user_input
    )

    execute_pipeline(stages)


if __name__ == "__main__":
    main()
