{ pkgs, lib, config, inputs, ... }:

{
  languages.python = {
    enable = true;
    package = pkgs.python311;
  };
  packages = with pkgs; [
    gnumake
    python311Packages.shellescape
  ];
  env.DJANGO_DEBUG = "1";

  processes.web.exec = "make dev";
}
