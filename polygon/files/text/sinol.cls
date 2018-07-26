%The MIT License (MIT)
%
%Copyright (c) 2014 Karol Farbiś, Marek Sommer
%
%Permission is hereby granted, free of charge, to any person obtaining a copy
%of this software and associated documentation files (the "Software"), to deal
%in the Software without restriction, including without limitation the rights
%to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
%copies of the Software, and to permit persons to whom the Software is
%furnished to do so, subject to the following conditions:
%
%The above copyright notice and this permission notice shall be included in all
%copies or substantial portions of the Software.
%
%THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
%IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
%FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
%AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
%LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
%OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
%SOFTWARE.

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{sinol}[2014/02/10]

\LoadClass[10pt, a4paper]{article}
\RequirePackage{polski}
\RequirePackage[utf8]{inputenc}
\RequirePackage{fancyhdr}
\RequirePackage{lastpage}
\RequirePackage{verbatim}
\RequirePackage[margin=2cm, a4paper, bottom=4.5cm]{geometry}
\RequirePackage{amsmath}
\RequirePackage{graphicx}
\RequirePackage{titlesec}

\newcommand{\RAM@}{BRAK RAMU}
\newcommand{\data@}{BRAK DATY}
\newcommand{\nazwa@}{BRAK NAZWY}
\newcommand{\kontest@}{BRAK KONKURSU}
\newcommand{\ID}{XXX}

\newcommand{\id}[1]{\renewcommand{\ID}{#1}}
\newcommand{\signature}[1]{}
\newcommand{\iomode}[1]{}
\renewcommand{\day}[1]{}
\newcommand{\RAM}[1]{\renewcommand{\RAM@}{#1}}
\renewcommand{\date}[1]{\renewcommand{\data@}{#1}}
\renewcommand{\title}[1]{\renewcommand{\nazwa@}{#1}}
\newcommand{\konkurs}[1]{\renewcommand{\kontest@}{#1}}

\fancyhead{}
\fancyfoot{}

\fancyhead[L]{\kontest@}
\fancyhead[C]{\includegraphics[width=2cm]{logo.pdf}}
\fancyhead[R]{\data@}
\fancyfoot[R]{\textit{\nazwa@}}
\fancyfoot[C]{\textit{\thepage/\pageref{LastPage}}}

\pagestyle{fancy}

\setlength{\headheight}{70pt}
\setcounter{secnumdepth}{0}

\setlength\parindent{0pt}
\setlength\parskip{10pt}

\titlespacing{\section}{0pt}{-3pt}{-3pt}
\titleformat{\subsection}{\bf}{}{0pt}{}
\titlespacing{\subsection}{9pt}{-3pt}{0pt}

\newenvironment{tasktext}{%startproblex
{%
\vspace*{-40pt}\noindent%
Dostępna pamięć: \RAM@{}MB%
\begin{center}%
\vspace*{3ex}%
\vspace*{-10pt}%
\textit{ \Huge \nazwa@ }%
\vspace*{-10pt}%
\vspace*{-10pt}%
\vspace*{3ex}%
\end{center}%
%
\noindent%
}%
}{}

\newcommand\twocol[2]{%
\begin{center}%
\begin{minipage}[t]{0.5\textwidth}%
\vspace{0pt}%
{#1}%
\end{minipage}\hfill%
\begin{minipage}[t]{0.5\textwidth}%
\vspace{0pt}%
{#2}%
\end{minipage}%
\end{center}}

\newcommand{\includefile}[1]{%
\vspace*{-3ex}%
\verbatiminput{#1}%
\vspace*{-4ex}%
}

\newcommand{\makeexamplef}[2]{%
\begin{tabular}{|p{0.47\textwidth}|p{0.47\textwidth}|}%
\hline%
\centering \texttt{Wejście} & \centering\let\\\tabularnewline\texttt{Wyjście} \\%
\hline%
\includefile{#1} & \includefile{#2} \\%
\hline%
\end{tabular}\\[2ex]%
}

\newcommand{\makeexample}[1]{\makeexamplef{#1.in}{#1.out}}
\newcommand{\makeexamplex}[1]{\makeexamplef{#1.in}{#1x.out}}

\renewcommand\t\texttt
\newcommand{\makecompactexample}{\section{Przykład}\makeexample0}
