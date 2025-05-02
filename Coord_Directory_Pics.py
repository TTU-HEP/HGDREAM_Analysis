import pandas as pd
import os
import re
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


csv_path = r"C:/Users/miles/APD/Connector_Pix/coord_directory_file/Coord_Directory_half.csv"
image_dir = r"C:/Users/miles/APD/Connector_Pix"

df = pd.read_csv(csv_path, encoding='utf-8-sig', delimiter=",", header=0)
df.columns = [col.strip().replace('\ufeff', '') for col in df.columns]

while True:
    print("\nEnter the coordinate.")
    print("General: Quarter_PCBletter_SiPM#")
    print("Example: 1_A_1")

    input_coord = input("Coordinate: ").strip()

    
    if input_coord[-1] in ['P', 'S', 'Q']:
        input_coord = input_coord[:-1]


    match = df[df.iloc[:, 0].str.startswith(input_coord, na=False)]

    if match.empty:
        print("No rod found for this coordinate.")
    else:
        row = match.iloc[0]  
        coord = row.iloc[0]
        rod_number = row.iloc[1] if pd.notna(row.iloc[1]) else "No rod number"
        print(f"\nCoordinate: {coord}")
        print(f"Rod Number: {rod_number}")

        issues = ['Broken', 'Recessed', 'Excessed', 'Glue_on_Fibers']
        for i, issue in enumerate(issues, start=2):
            if str(row.iloc[i]).strip().lower() == 'x':
                print(f"- {issue}")

       
        if rod_number != "No rod number":
            rod_number_float = float(rod_number)
            if rod_number_float.is_integer():
                rod_number_str = str(int(rod_number_float))  
            else:
                rod_number_str = str(rod_number_float)  
        else:
            rod_number_str = None

        while True:
            user_input = input("Press Enter to view rod images, or 'q' to quit: ").strip().lower()
            if user_input == 'q':
                print("Exiting...")
                exit()

            if rod_number_str is None:
                print("No rod number to search for images.")
                break

            valid_exts = ('.jpg', '.png')
            rod_pattern = re.compile(rf'(?<!\d)0*{re.escape(rod_number_str)}(?!\.\d)(?=[^0-9]|\b)', re.IGNORECASE)

            found_images = [
                f for f in os.listdir(image_dir)
                if f.lower().endswith(valid_exts)
                and not f.startswith("._")
                and rod_pattern.search(f)
            ]

            if not found_images:
                print("No images found for this rod.")
                break

            for image_file in found_images:
                print(f"\nDisplaying image: {image_file}")
                if re.search(r'\(s\)|[^a-zA-Z]s[^a-zA-Z]?', image_file, re.IGNORECASE):
                    print("Rod Type: Scintillating")
                elif 'P' in image_file:
                    print("Rod Type: Plastic")
                elif 'Q' in image_file:
                    print("Rod Type: Quartz")
                else:
                    print("Rod Type: Unknown")

                img_path = os.path.join(image_dir, image_file)
                img = mpimg.imread(img_path)
                plt.imshow(img)
                plt.title(image_file)
                plt.axis('off')
                plt.show()
            break  

    again = input("\nWould you like to input another coordinate? (y/n): ").strip().lower()
    if again != 'y':
        print("Exiting...")
        break















