from ecc.cellfinder import CellFinder
import easygui
from easygui import EgStore
import sys, os.path


class Settings(EgStore):
    def __init__(self, filename="settings_find_objects.txt"):
        self.vx = 6.45
        self.vy = 6.45
        self.vz = 7.0
        self.bsize = 120
        self.overlap = 20
        self.threshold = 0.70
        self.minvol = 2
        self.maxvol = 64
        self.intensity_mode = "obj_mean"
        
        self.rawimg = ""
        self.probimg = ""
        self.out_csv = ""
        
        self.filename = filename
        self.restore()

def exit_if_none(var):
    if var is None:
        print("Cancelled")
        sys.exit(0)


if __name__ == "__main__":
    settings = Settings()
    
    # create a new instance
    cf = CellFinder()

    # force it print detailed progress
    cf.set_verbose(True)

    # Optional: set number of parallel CPU cores
    #cf.set_num_workers(1)

    field_values = [
        settings.vx,
        settings.vy,
        settings.vz,
        settings.bsize,
        settings.overlap,
        settings.threshold,
        settings.minvol,
        settings.maxvol,
        settings.intensity_mode,
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
        "mode (obj_mean or max)"
    ]

    msg = "Enter parameters:\n"
    err_msg = ""
    while True:
        field_values = easygui.multenterbox(msg+err_msg, "Setting", labels, 
                                            [str(f) for f in field_values])
        print("values:", field_values)
        if field_values is None:
            print("Cancelled")
            sys.exit(0)

        err_msg = ""
        try:
            settings.vx = float(field_values[0])
            settings.vy = float(field_values[1])
            settings.vz = float(field_values[2])
        except ValueError:
            err_msg += "voxel size must be decimal numbers\n"
            
        try:
            settings.bsize = int(field_values[3])
            settings.overlap = int(field_values[4])
        except ValueError:
            err_msg += "blocksize and overlap must be integers\n"

        try:
            settings.threshold = float(field_values[5])
        except ValueError:
            err_msg += "threshold must be a decimal number\n"

        try:
            settings.minvol = int(field_values[6])
            settings.maxvol = int(field_values[7])
        except ValueError:
            err_msg += "min/max volume must be integers\n"

        if field_values[8] not in ["obj_mean", "max"]:
            err_msg += "mode must be 'obj_mean' or 'max'"
        else:
            settings.intensity_mode = field_values[8]

        if err_msg == "":
            settings.store()
            break

    # set voxel size of the input image
    cf.set_image_voxel_size( {"X": settings.vx, "Y": settings.vy, "Z": settings.vz} )

    # Optional: set block size
    cf.set_block_size({"blocksize": settings.bsize, "overlap": settings.overlap})

    # set some parameters
    cf.set_prob_threshold(settings.threshold)
    cf.set_min_particle_volume(settings.minvol)
    cf.set_max_particle_volume(settings.maxvol)
    cf.set_intensity_computation_mode(settings.intensity_mode)

    settings.rawimg = easygui.fileopenbox(
        title="Select raw image:",
        filetypes=["*.hdf5", "*.h5"],
        default=settings.rawimg
    )
    exit_if_none(settings.rawimg)
    print("raw img: " + settings.rawimg)
    settings.store()
    cf.set_raw_image_path(settings.rawimg)

    settings.probimg = easygui.fileopenbox(
        title="Select probability image:",
        filetypes=["*.hdf5", "*.h5"],
        default=settings.probimg
    )
    exit_if_none(settings.probimg)
    print("prob img: " + settings.probimg)
    settings.store()
    cf.set_prob_image_path(settings.probimg)

    settings.out_csv = easygui.filesavebox(
        title="Set output csv:",
        default=settings.out_csv if settings.out_csv else os.path.join(os.path.dirname(settings.probimg), "cells_table.csv"),
        filetypes=["*.csv"]
    )
    exit_if_none(settings.out_csv)
    if os.path.splitext(settings.out_csv)[1] == "":
        settings.out_csv += ".csv"
    print("out csv: " + settings.out_csv)
    settings.store()
    cf.set_savename(settings.out_csv)

    # run!
    try:
        cf.run_main()
    except:
        easygui.exceptionbox()
    else:
        easygui.msgbox("Successfully finished!")
