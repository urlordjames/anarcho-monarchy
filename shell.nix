{ pkgs ? import (fetchTarball https://github.com/urlordjames/nixpkgs/archive/nixos-unstable.tar.gz) {} }:
let dependancies = python-packages: with python-packages; [
  django
  user-agents
  django-user-agents
  psycopg2
  requests
];
in pkgs.mkShell {
  buildInputs = with pkgs; [
    (python3.withPackages dependancies)
  ];
}
