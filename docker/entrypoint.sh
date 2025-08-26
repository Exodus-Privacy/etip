#!/bin/bash

declare -r pyexe=python3
declare -r pymanage="$pyexe manage.py"
declare -r custom_docker_settings="/etip/etip/etip/settings/custom_docker.py"

declare -Ar commandList=(
	[collect-static]=collectStatic
	[compare-with-exodus]=compareWithExodus
	[compile-messages]=compileMessages
	[create-db]=createDB
	[create-user]=createUser
	[import-trackers]=importTrackers
	[init]=init
	[make-messages]=makeMessages
	[start-etip]=startEtip
	[test]=test
)

declare -Ar commandHelpList=(
	[collect-static]='collect all static files'
	[compare-with-exodus]='looks for differences with εxodus and local trackers'
	[compile-messages]='compile translation messages'
	[create-db]='create database if required and attend to migrations'
	[create-user]='actually create a super user if not created yet'
	[import-trackers]='import trackers from the official exodus instance'
	[init]='Initialize database and launch ETIP'
	[make-messages]='extract translation messages'
	[start-etip]='lauch the local etip'
	[test]='run tests'
)

function main()
{
	getSettings

	if [ -z "$1" ]
	then
		usage "$0"
	elif [ -n "${commandList[$1]}" ]
	then
		"${commandList[$1]}"
	else
		exec "$@"
	fi
}

function usage()
{
	cat <<- EOS
		$1: prepare and lauch etip

	EOS

	for cmd in "${!commandHelpList[@]}"
	do
		cat <<- EOS
			$cmd: ${commandHelpList[$cmd]}
		EOS
	done
}

function getSettings() {
	if [ -f "$custom_docker_settings" ]; then
		export DJANGO_SETTINGS_MODULE=etip.settings.custom_docker
	else
		export DJANGO_SETTINGS_MODULE=etip.settings.docker
		cat <<- EOS
		File ${custom_docker_settings} doesn't exist, you might want to create it:

			from .docker import *

			DEBUG=True
			SECRET_KEY = "<a unique secret for Django>"
		EOS
	fi
}

function createDB() {
	$pymanage migrate
}

function createUser() {
	$pymanage createsuperuser
}

function collectStatic() {
	$pymanage collectstatic --noinput
}

function startEtip() {
	exec $pymanage runserver 0.0.0.0:8000
}

function importTrackers() {
	$pymanage import_trackers
	$pymanage import_categories
}

function makeMessages() {
	$pymanage makemessages
}

function compareWithExodus() {
	$pymanage compare_with_exodus
}

function compileMessages() {
	$pymanage compilemessages
}

function test() {
	$pymanage test
}

function init() {
	createDB
	importTrackers
	echo "ETIP DB is ready."
	startEtip
}

main "$@"
