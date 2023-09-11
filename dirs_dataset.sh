#!/bin/zsh

# The main directory containing all category directories
ORIGINAL_DIR="/Users/a123/proj/genePaper/dsp/Dataset"
# The directory where you want to create symbolic links to all subcategories
LINK_DIR="/Users/a123/proj/genePaper/dsp/Links"

# Create the LINK_DIR if it doesn't exist
mkdir -p $LINK_DIR

# Loop through each category and subcategory to create symbolic links
for category in $(ls $ORIGINAL_DIR); do
    for subcategory in $(ls $ORIGINAL_DIR/$category); do
        # Create a symbolic link to the subcategory in the LINK_DIR
        ln -s $ORIGINAL_DIR/$category/$subcategory $LINK_DIR/${subcategory}_from_$category
    done
done
