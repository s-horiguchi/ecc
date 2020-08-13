from ecc.ilastik_wrapper import PixelClassifier
import easygui
from easygui import EgStore
import sys, os.path


class Settings(EgStore):
    def __init__(self, filename="settings_apply_classifier.txt"):
        self.ilastik_dir = "c:/Program Files/ilastik-1.3.3post3"
        self.projfile = ""
        self.rawimg = ""
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
    settings.rawimg = easygui.fileoepnbox(
        title="Select raw image:",
        filetypes=["*.hdf5", "*.h5"],
        default=settings.rawimg
    )
    exit_if_none(settings.rawimg)
    print("raw img:", settings.rawimg)
    settings.store()
    pc.set_input_image(settings.rawimg)

    # define output
    settings.outdir = easygui.diropenbox(
        title="Select output directory:",
        default=settings.outdir if settings.outdir else os.path.dirname(rawimg)
    )
    exit_if_none(settings.outdir)
    print("out dir:", settings.outdir)
    settings.store()
    pc.set_output_dir(settings.outdir)

    # run!
    pc.run()
