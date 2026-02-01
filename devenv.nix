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
}
