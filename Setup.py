from py2exe.build_exe import Target, build_exe

# Define your target
target = Target(
    script="path_to_your_main_script.py",
    dest_base="name_of_executable",
    # include other parameters as needed
)

# Create a build object
build = build_exe(
    options={
        "bundle_files": 1,  # Bundle everything into one exe
        "compressed": True,  # Compress the library archive
        # include other options as needed
    },
    targets=[target],
)

# Run the build
build()
