from ecc.ilastik_wrapper import PixelClassifier
from ecc.cellfinder import CellFinder
import easygui
from easygui import EgStore
import sys, os.path, glob
import multiprocessing as mp
import subprocess as sp


class Settings(EgStore):
    def __init__(self, filename="settings_ecc.txt"):
        ilastik_list = glob.glob("c:/Program Files/ilastik-*")
        self.ilastik_dir = ilastik_list[0] if ilastik_list else ""
        self.projfile = ""
        self.rawimg = ""
        self.out_probimg = ""
        
        
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

def apply_classifier(settings):
        # create a new instance
    pc = PixelClassifier()

    # force it print detailed progress
    pc.set_verbose(True)

    # set ilastik path
    while not os.path.exists(os.path.join(settings.ilastik_dir, "ilastik.exe")):
        print("ilastik dir is invalid. please select ilastik path")
        settings.ilastik_dir = easygui.diropenbox(
            title="Select ilastik path:",
            default=settings.ilastik_dir
        )
        exit_if_none(settings.ilastik_dir)
        settings.store()
    print("ilastik dir:", settings.ilastik_dir)
    pc.set_ilastik_executable_path(settings.ilastik_dir)

    # set path to ilastik project
    settings.projfile = easygui.fileopenbox(
        title="Select ilastik project file",
        filetypes=["*.ilp"],
        default=settings.projfile
    )
    exit_if_none(settings.projfile)
    print("project file:", settings.projfile)
    settings.store()
    pc.set_project_file(settings.projfile)

    # Optional: control CPU and memory usage
    #pc.set_num_threads(20)
    #pc.set_max_memory_size(60000) # in MBs

    # define input image
    settings.rawimg = easygui.fileopenbox(
        title="Select raw image:",
        filetypes=["*.hdf5", "*.h5"],
        default=settings.rawimg
    )
    exit_if_none(settings.rawimg)
    print("raw img:", settings.rawimg)
    settings.store()
    pc.set_input_image(settings.rawimg)

    # define output
    settings.out_probimg = easygui.filesavebox(
        title="Set output probability image:",
        default=settings.out_probimg if settings.out_probimg else os.path.join(os.path.dirname(settings.rawimg), "prob_image.h5"),
        filetypes=["*.hdf5", "*.h5"]
    )
    exit_if_none(settings.out_probimg)
    if os.path.splitext(settings.out_probimg)[1] == "":
        settings.out_probimg += ".h5"
    print("out probability img:", settings.out_probimg)
    settings.store()
    pc.set_output_image(settings.out_probimg)

    # run!
    try:
        pc.run()
    except RuntimeError:
        easygui.exceptionbox()
    else:
        easygui.msgbox("Successfully finished!")

def find_objects(settings):
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
        settings.threshold,
        settings.minvol,
        settings.maxvol,
        settings.intensity_mode,
        settings.bsize,
        settings.overlap,
    ]
    labels = [
        "Voxel size(x) in um",
        "Voxel size(y) in um",
        "Voxel size(z) in um",
        "Threshold",
        "Min volume in voxel",
        "Max volume in voxel",
        "Mode (obj_mean or max)",
        "Blocksize",
        "Overlap"
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
            settings.threshold = float(field_values[3])
        except ValueError:
            err_msg += "threshold must be a decimal number\n"

        try:
            settings.minvol = int(field_values[4])
            settings.maxvol = int(field_values[5])
        except ValueError:
            err_msg += "min/max volume must be integers\n"

        if field_values[6] not in ["obj_mean", "max"]:
            err_msg += "mode must be 'obj_mean' or 'max'"
        else:
            settings.intensity_mode = field_values[6]

        try:
            settings.bsize = int(field_values[7])
            settings.overlap = int(field_values[8])
        except ValueError:
            err_msg += "blocksize and overlap must be integers\n"

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


if __name__ == "__main__":
    mp.freeze_support()

    # restore settings
    settings = Settings()

    choices = [
        "Start ilastik",
        "Apply classifier",
        "Find Objects"
    ]

    while True:
        selected = easygui.choicebox(
            msg="Welcome to ecc!",
            title="ecc",
            choices=choices
        )

        exit_if_none(selected)
        if selected == choices[0]:
            # start ilastik in the background
            while True:
                path = os.path.join(settings.ilastik_dir, "ilastik.exe")
                if os.path.exists(path): break

                print("ilastik dir is invalid. please select ilastik path")
                settings.ilastik_dir = easygui.diropenbox(
                    title="Select ilastik path:",
                    default=settings.ilastik_dir
                )
                exit_if_none(settings.ilastik_dir)
                settings.store()
            print("ilastik dir:", settings.ilastik_dir)            
            p = sp.Popen(path)
            print("Started ilastik [PID={}]".format(p.pid))

        elif selected == choices[1]:
            apply_classifier(settings)
        elif selected == choices[2]:
            find_objects(settings)
