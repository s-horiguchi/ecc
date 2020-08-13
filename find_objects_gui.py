from ecc.cellfinder import CellFinder
import easygui
import sys

if __name__ == "__main__":
    # create a new instance
    cf = CellFinder()

    # force it print detailed progress
    cf.set_verbose(True)

    # Optional: set number of parallel CPU cores
    #cf.set_num_workers(4)

    field_values = [
        6.45, 6.45, 7.0, # voxel size
        120, 20,# blocksize
        0.70,   # threshold
        2,      # min volume
        64,     # max volume
        "test", #nickname   
    ]
    labels = [
        "voxel size(x)",
        "voxel size(y)",
        "voxel size(z)",
        "blocksize",
        "overlap",
        "threshold",
        "min volume",
        "max volume",
        "nickname",
    ]

    msg = "Enter parameters:\n"
    err_msg = ""
    while True:
        print(field_values)
        field_values = easygui.multenterbox(msg+err_msg, "Setting", labels, 
                                            [str(f) for f in field_values])
        print(field_values)
        if field_values is None:
            print("Cancelled")
            sys.exit(1)

        err_msg = ""
        try:
            vx = float(field_values[0])
            vy = float(field_values[1])
            vz = float(field_values[2])
        except ValueError:
            err_msg += "voxel size must be decimal numbers\n"
            
        try:
            bsize = int(field_values[3])
            overlap = int(field_values[4])
        except ValueError:
            err_msg += "blocksize and overlap must be integers\n"

        try:
            threshold = float(field_values[5])
        except ValueError:
            err_msg += "threshold must be a decimal number\n"

        try:
            minvol = int(field_values[6])
            maxvol = int(field_values[7])
        except ValueError:
            err_msg += "min/max volume must be integers\n"

        nickname = field_values[8]
        if err_msg == "":
            break

    # set voxel size of the input image
    cf.set_image_voxel_size( {"X": vx, "Y": vy, "Z": vz} )

    # Optional: set block size
    cf.set_block_size({"blocksize": bsize, "overlap": overlap})

    # set some parameters
    cf.set_prob_threshold(threshold)
    cf.set_min_particle_volume(minvol)
    cf.set_max_particle_volume(maxvol)
    cf.set_intensity_computation_mode('obj_mean')

    # give it a nice nickname
    cf.set_nickname(nickname)


    outdir = easygui.diropenbox("Select output directory:")
    rawimg = easygui.fileopenbox("Select raw image:")
    probimg = easygui.fileopenbox("Select probability image:")

    print("outdir: " + outdir)
    print("raw img: " + rawimg)
    print("prob img: " + probimg)

    # set output directory
    cf.set_outdir(outdir)
    cf.set_raw_image_path(rawimg)
    cf.set_prob_image_path(probimg)

    # run!
    cf.run_main()
