from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.scm import Version
from conan.tools.build import check_min_cppstd
import re
import os

def get_version():
    try:
        with open("CMakeLists.txt") as f:
            content = f.read()
        version = re.search(r"^\s*project\(ozo\s+VERSION\s+([^\s)]+)", content, re.M).group(1)
        return version.strip()
    except Exception:
        return None

class OzoConan(ConanFile):
    name = "ozo"
    version = get_version()
    license = "PostgreSQL"
    topics = ("ozo", "yandex", "postgres", "postgresql", "cpp17", "database", "db", "asio")
    url = "https://github.com/yandex/ozo"
    description = "Conan package for yandex ozo"
    settings = "os", "compiler", "build_type", "arch"

    exports_sources = "include/*", "CMakeLists.txt", "cmake/*", "LICENSE", "AUTHORS"

    generators = "CMakeDeps", "CMakeToolchain"

    requires = (
        "boost/1.79.0",
        "resource_pool/cci.20210322",
        "libpq/15.12"
    )

    def layout(self):
        cmake_layout(self)

    def validate(self):
        #if self.settings.os == "Windows":
        #    raise Exception("OZO is not compatible with Windows")
        if self.settings.get_safe("compiler.cppstd"):
            check_min_cppstd(self, 17)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_id(self):
        self.info.clear()  # аналог header_only()

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.requires = [
            "boost::boost", "boost::system", "boost::thread", "boost::coroutine",
            "resource_pool::resource_pool", "libpq::pq"
        ]
        self.cpp_info.defines = [
            "BOOST_COROUTINES_NO_DEPRECATION_WARNING",
            "BOOST_HANA_CONFIG_ENABLE_STRING_UDL",
            "BOOST_ASIO_USE_TS_EXECUTOR_AS_DEFAULT"
        ]

        compiler = self.settings.compiler
        version = Version(str(compiler.version))
        if str(compiler) in ["clang", "apple-clang"] or (str(compiler) == "gcc" and version >= "9"):
            self.cpp_info.cxxflags = [
                "-Wno-gnu-string-literal-operator-template",
                "-Wno-gnu-zero-variadic-macro-arguments",
            ]
