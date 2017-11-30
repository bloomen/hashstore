cmake_minimum_required(VERSION 2.8)
project(hashstore)

add_executable(hashstore src/main.cpp)

target_link_libraries(hashstore served boost_system boost_serialization)

if (MSVC)
   set(CMAKE_CXX_FLAGS "/W4 /WX /bigobj /EHsc /wd4503 /wd4996 /wd4702")
else()
   set(CMAKE_CXX_FLAGS "-std=c++11 -pedantic -Wall -Wextra -Wconversion")
   if (CMAKE_COMPILER_IS_GNUCC)
      set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread")
   endif()
   target_link_libraries(hashstore ${CMAKE_THREAD_LIBS_INIT})
endif()
