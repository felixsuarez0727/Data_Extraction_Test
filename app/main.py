from runners import run_scraper, run_cleanup, run_database, run_image_processing, run_csv_generation

if __name__ == "__main__":

    # Cleanup older files
    run_cleanup()
    # Create empty database
    run_database()
    # Populate database with web data
    run_scraper()
    # Process and create images
    run_image_processing()
    # Genearate CSV
    run_csv_generation()
