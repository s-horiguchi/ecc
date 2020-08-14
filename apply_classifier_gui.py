from ecc.ilastik_wrapper import PixelClassifier
import easygui
from easygui import EgStore
import sys, os.path, glob


class Settings(EgStore):
    def __init__(self, filename="settings_apply_classifier.txt"):
        ilastik_list = glob.glob("c:/Program Files/ilastik-*")
        self.ilastik_dir = ilastik_list[0] if ilastik_list else ""
        self.projfile = ""
        self.rawimg = ""
        self.out_probimg = ""
        
        self.filename = filename
        self.restore()

def exit_if_none(var):
    if var is None:
        print("Cancelled")
        sys.exit(0)

if __name__ == "__main__":
    settings = Settings()
    
    # create a new instance
    pc = PixelClassifier()

    # force it print detailed progress
    pc.set_verbose(True)

    # set ilastik path
    settings.ilastik_dir = easygui.diropenbox(
        title="Select ilastik path:",
        default=settings.ilastik_dir
    )
    exit_if_none(settings.ilastik_dir)
    print("ilastik dir:", settings.ilastik_dir)
    settings.store()
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
