<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Project Information

This is a Python Flask web application for a Local Files Sharing Platform (LFSP) that provides a safer alternative to USB file sharing. Key components:

1. Flask backend to handle file sharing operations
2. Tailwind CSS for UI design
3. In-memory storage for links and shared devices
4. Features: sharing links, password protection, expiration times, read-only access


# Software Requirements Specification (SRS) Document: LFSP - Local Files Sharing Platform

# Version: 1.0 Date: April 24, 2025 Author: nadeeshafdo

# 1. Introduction

# 1.1 Purpose

This document details the software requirements for LFSP (Local Files Sharing Platform), a software solution designed to provide a safer, more convenient, and more versatile alternative to directly connecting external storage devices via USB. This SRS document will serve as a guide for developers, testers and stakeholders throughout the development lifecycle.

## 1.2 Scope

LFSP will enable users to share files and folders from a selected storage device (HDD, SSD, USB drive) over a network, eliminating the need for direct USB connections. It will support multiple platforms (Windows, macOS, Linux) and provide secure access control.

# 1.3 Intended Audience

This document is intended for:

Software Developers

Software Testers

Project Managers

Stakeholders

Coding LLMs

# 1.4 Definitions, Acronyms and Abbreviations

LFSP: Local Files Sharing Platform

HDD: Hard Disk Drive

SSD: Solid State Drive

API: Application Programming Interface

SRS: Software Requirements Specification

HTTP: Hypertext Transfer Protocol

HTTPS: HTTP Secure

# 2. Overall Description

## 2.1 Product Perspective

LFSP is a standalone application that will operate on the user's local machine. It will not require any external services or cloud dependencies for core functionality. The primary goal is to provide a secure and reliable mechanism for network-based file sharing, mitigating the risks associated with direct USB connections.

## 2.2 Product Functions

Storage Selection: Allow users to select a storage device (HDD, SSD, USB drive) or specific partitions/folders on that device to share.

Link Generation: Generate secure, temporary links providing network access to the selected storage.

Access Control: Implement read-only access to shared storage by default, with optional password protection.

Platform Support: Provide native applications for Windows, macOS, and Linux.

Configuration: Allow users to configure port numbers, shared directories, and security parameters.

# 2.3 User Classes and Characteristics

General User: Tech-savvy individuals who want a more convenient and secure way to share files from their external storage. Little to no technical expertise required.

Advanced User: Users who require more control over configuration options and security settings. Comfortable with command-line interfaces and configuration files.

# 2.4 Operating Environment

Operating Systems: Windows 10/11, macOS 10.15+, Linux (various distributions).

Network: TCP/IP network (local network or internet connection).

Hardware: Standard PC/Laptop/Server hardware.

# 2.5 Design and Implementation Constraints

Cross-platform compatibility is a key requirement.

Security must be a primary consideration.

The application should be lightweight and resource-efficient.

Minimal dependencies on external libraries.

# 3. Specific Requirements

3.1 Functional Requirements


| ID  | Description  | Priority  | Priority  |
| --- | --- | --- | --- |
| FR01  | Allow users to select a storage device/partition. | High  | High  |
| FR02  | Generate a unique, temporary link for access.  | High  | High  |
| FR03  | Enforce read-only access to shared storage.  | High  | High  |
| FR04  | Allow users to set a password for the shared<br>link.  | Medium  | Medium  |
| FR05 ID  | Allow users to set an expiration time for the link. Description  | Allow users to set an expiration time for the link. Description  | Medium Priority  |
| FR06  | Display the status of shared devices/links. | Display the status of shared devices/links. | Medium  |
| FR07  | Support multiple concurrent connections.  | Support multiple concurrent connections.  | Low  |
