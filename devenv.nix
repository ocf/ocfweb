{ pkgs, lib, config, inputs, ... }:

{
  languages.python = {
    enable = true;
    version = "3.11";
  };
  packages = with pkgs; [
    gnumake
    python312Packages.shellescape
  ];
  env.DJANGO_DEBUG = "1";

  processes.web.exec = "make dev";
}
