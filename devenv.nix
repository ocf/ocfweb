{ pkgs, lib, config, inputs, ... }:

{
  cachix.enable = false;
  languages.python = {
    enable = true;
    package = pkgs.python311;
    venv = {
      enable = true;
      requirements = builtins.readFile ./requirements.txt + builtins.readFile ./requirements-dev.txt;
    };
    uv.enable = true;
  };
  packages = with pkgs; [
    gnumake
  ];
  env.DJANGO_DEBUG = "1";

  processes.web.exec = "make dev";

  enterShell = ''
    git submodule update --init
  '';
}
