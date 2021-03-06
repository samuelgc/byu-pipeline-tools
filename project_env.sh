export BYU_PROJECT_DIR=/groups/dusk
export BYU_TOOLS_DIR=/groups/dusk/byu-pipeline-tools

# python 2.7
export PYTHONPATH=${PYTHONPATH}:/usr/lib64/python2.7:/usr/lib64/python2.7/plat-linux2:/usr/lib64/python2.7/lib-old:/usr/lib64/python2.7/lib-dynload:/usr/lib64/python2.7/site-packages:/usr/lib/python2.7/site-packages
# maya python
# export PYTHONPATH=${PYTHONPATH}:/usr/autodesk/maya/lib/python2.7/site-packages
# houdini python
export PYTHONPATH=${PYTHONPATH}:/opt/hfs.current/houdini/python2.7libs

# byu tools
export MAYA_SHELF_DIR=${BYU_TOOLS_DIR}/maya-tools/shelf

export PYTHONPATH=${PYTHONPATH}:${BYU_TOOLS_DIR}
export PATH=${PATH}:${BYU_TOOLS_DIR}/bin

