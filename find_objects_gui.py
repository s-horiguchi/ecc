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
        self.nickname = "test"
        self.intensity_mode = "obj_mean"
        
        self.rawimg = ""
        self.probimg = ""
        self.outdir = ""
        
        self.filename = filename
        self.restore()

def exit_if_none(var):
    if var is None:
        print("Cancelled")
        sys.exit(1)


if __name__ == "__main__":
    settings = Settings()
    
    # create a new instance
    cf = CellFinder()

    # force it print detailed progress
    cf.set_verbose(True)

    # Optional: set number of parallel CPU cores
    #cf.set_num_workers(4)

    field_values = [
        settings.vx,
        settings.vy,
        settings.vz,
        settings.bsize,
        settings.overlap,
        settings.threshold,
        settings.minvol,
        settings.maxvol,
        settings.nickname
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
        field_values = easygui.multenterbox(msg+err_msg, "Setting", labels, 
                                            [str(f) for f in field_values])
        print("values:", field_values)
        if field_values is None:
            print("Cancelled")
            sys.exit(1)

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

        settings.nickname = field_values[8]
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

    # give it a nice nickname
    cf.set_nickname(settings.nickname)

    settings.rawimg = easygui.fileopenbox(
        title="Select raw image:",
        filetypes=["*.hdf5", "*.h5"],
        default=settings.rawimg
    )
    exit_if_none(settings.rawimg)
    settings.probimg = easygui.fileopenbox(
        title="Select probability image:",
        filetypes=["*.hdf5", "*.h5"],
        default=settings.probimg
    )
    exit_if_none(settings.probimg)
    settings.outdir = easygui.diropenbox(
        title="Select output directory:",
        default=settings.outdir if settings.outdir else os.path.dirname(settings.probimg)
    )
    exit_if_none(settings.outdir)

    print("outdir: " + settings.outdir)
    print("raw img: " + settings.rawimg)
    print("prob img: " + settings.probimg)
    settings.store()
    
    # set output directory
    cf.set_outdir(settings.outdir)
    cf.set_raw_image_path(settings.rawimg)
    cf.set_prob_image_path(settings.probimg)

    # run!
    cf.run_main()
