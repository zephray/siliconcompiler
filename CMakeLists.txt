cmake_minimum_required(VERSION 3.14...3.16)

project(siliconcompiler VERSION "0.0.1")

# Add OpenROAD, but exclude all targets by default
add_subdirectory(third_party/tools/openroad/tools/OpenROAD/ EXCLUDE_FROM_ALL)
# Manually enable opendbpy target
set_target_properties(opendbpy PROPERTIES EXCLUDE_FROM_ALL 0)

# Install opendbpy
install(TARGETS opendbpy DESTINATION .)
