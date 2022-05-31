import subprocess as ps

import logging

#logging.basicConfig(level=logging.DEBUG,filename="part.log",format='%(asctime)s:%(levelname)s:%(message)s')

logger= logging.getLogger("Disk_partition")

logger.setLevel(level=logging.DEBUG)
formatter= logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler=logging.FileHandler("part.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class Disk_partition:

    def __init__(self,dev_name):
        self.dev_name = dev_name

    #creating partition
    def cre_partition(self,dev_type:str,start:str,end:str):
        partition=ps.run(f"parted -a opt {self.dev_name} mkpart primary {dev_type}{start}{end}", shell=True, capture_output=True, text=True)
        if partition.returncode == 0:
            logging.info("partition created sucessfully")
        else:
            logging.error(partition.stderr)
    #partition details
    def part_details(self):
        details= ps.run(f"fdisk -l{self.dev_name}",shell=True,capture_output=True,text=True)
        if details.returncode==0:
            logging.info("partition details: \n",details)
        else:
            logging.error(details.stderr)

    def formatting(self,part_name,part_type):
        file=ps.run(f"mkfs -t {part_type} {part_name}",shell=True,capture_output=True,text=True)
        if file.returncode==0:
            logging.info("%s is formatted to %s",part_name,part_type)
        else:
            logging.error(file.stderr)
    def mounting(self,part_name,mount_dir):
        mount=ps.run(f"mount {part_name}{mount_dir}",shell=True,capture_output=True,text=True)
        if mount.returncode==0:
            logging.info("mounted %s disk to dir %s",part_name,mount_dir)
        else:
            logging.error(mount.stderr)

if __name__ == "__main__":
    device =Disk_partition("/dev/sdc")

    device.cre_partition("ext4","0G","3G")
    device.formatting("/dev/sdc1","ext4")
    device.mounting("/dev/sdc1","disk")


    device.part_details()