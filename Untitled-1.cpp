#ifndef UNICODE
#define UNICODE
#endif

#ifndef _UNICODE
#define _UNICODE
#endif

#define _WIN32_IE 0x0600
#define WINVER 0x0601
#define _WIN32_WINNT 0x0601
#include <windows.h>
#include <commctrl.h>
#include <shlwapi.h>
#include <shellapi.h>
#include <shlobj.h>
#include <string>
#include <vector>
#include <algorithm>
#include <iomanip>
#include <sstream>

#pragma comment(lib, "comctl32.lib")
#pragma comment(lib, "shlwapi.lib")
#pragma comment(linker, "/manifestdependency:\"type='win32' name='Microsoft.Windows.Common-Controls' version='6.0.0.0' processorArchitecture='*' publicKeyToken='6595b64144ccf1df' language='*'\"")

// Global variables
HWND g_hWnd = NULL, g_hTreeView = NULL, g_hDirEdit = NULL, g_hStatusBar = NULL;
int g_sortColumn = 1; // Default to sort by size
bool g_sortAscending = true;
std::wstring g_currentPath;

// File item structure
struct FileItem {
    std::wstring name, fullPath;
    ULONGLONG size;
    FILETIME modified;
    bool isDirectory;
};

std::vector<FileItem> g_fileItems;

// Forward declarations
LRESULT CALLBACK WndProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam);
void CreateControls(HWND hwnd);
void PopulateTreeView(const std::wstring& path);
void SortItems();
void RefreshStatusBar();
std::wstring FormatFileSize(ULONGLONG size);
std::wstring FormatFileTime(const FILETIME& ft);
void HandleTreeViewClick(LPNMITEMACTIVATE pnmitem);
void NavigateToDirectory(const std::wstring& path);

// Sort items based on current sort criteria
void SortItems() {
    std::sort(g_fileItems.begin(), g_fileItems.end(), [](const FileItem& a, const FileItem& b) {
        if (a.isDirectory != b.isDirectory) return a.isDirectory;
        bool result = (g_sortColumn == 1) ? (a.size < b.size) : (CompareFileTime(&a.modified, &b.modified) < 0);
        return g_sortAscending ? result : !result;
    });
}

// Update the status bar with information about the current directory
void RefreshStatusBar() {
    int fileCount = 0, dirCount = 0;
    ULONGLONG totalSize = 0;
    for (const FileItem& item : g_fileItems) {
        if (item.isDirectory) dirCount++;
        else { fileCount++; totalSize += item.size; }
    }
    std::wstringstream ss;
    ss << L"Files: " << fileCount << L"  Folders: " << dirCount;
    if (fileCount > 0) ss << L"  Total size: " << FormatFileSize(totalSize);
    SendMessage(g_hStatusBar, SB_SETTEXT, 0, (LPARAM)ss.str().c_str());
}

// Format file size in a human-readable format
std::wstring FormatFileSize(ULONGLONG size) {
    const double KB = 1024.0, MB = 1024.0 * KB, GB = 1024.0 * MB, TB = 1024.0 * GB;
    std::wstringstream ss; ss << std::fixed << std::setprecision(2);
    if (size < KB) ss << size << L" bytes";
    else if (size < MB) ss << (size / KB) << L" KB";
    else if (size < GB) ss << (size / MB) << L" MB";
    else if (size < TB) ss << (size / GB) << L" GB";
    else ss << (size / TB) << L" TB";
    return ss.str();
}

// Format file time in a readable format
std::wstring FormatFileTime(const FILETIME& ft) {
    SYSTEMTIME st; FILETIME localFt;
    FileTimeToLocalFileTime(&ft, &localFt); FileTimeToSystemTime(&localFt, &st);
    wchar_t buffer[100];
    GetDateFormatEx(LOCALE_NAME_USER_DEFAULT, DATE_SHORTDATE, &st, NULL, buffer, 100, NULL);
    std::wstring dateStr = buffer;
    GetTimeFormatEx(LOCALE_NAME_USER_DEFAULT, TIME_NOSECONDS, &st, NULL, buffer, 100);
    return dateStr + L" " + buffer;
}

// Handle double-click on tree view item
void HandleTreeViewClick(LPNMITEMACTIVATE pnmitem) {
    if (pnmitem->iItem == -1) return;
    LVITEM lvi = { 0 }; lvi.mask = LVIF_PARAM; lvi.iItem = pnmitem->iItem;
    ListView_GetItem(g_hTreeView, &lvi);
    int index = static_cast<int>(lvi.lParam);
    if (index < 0 || index >= static_cast<int>(g_fileItems.size())) return;
    const FileItem& item = g_fileItems[index];
    if (item.isDirectory) NavigateToDirectory(item.fullPath);
    else ShellExecute(NULL, L"open", const_cast<LPWSTR>(item.fullPath.c_str()), NULL, NULL, SW_SHOWNORMAL);
}

// Navigate to a new directory
void NavigateToDirectory(const std::wstring& path) {
    g_currentPath = path;
    SetWindowText(g_hDirEdit, path.c_str());
    PopulateTreeView(path);
}

// Entry point
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    INITCOMMONCONTROLSEX icc = { sizeof(INITCOMMONCONTROLSEX), ICC_WIN95_CLASSES | ICC_DATE_CLASSES | ICC_USEREX_CLASSES };
    InitCommonControlsEx(&icc);
    WNDCLASSEX wcex = { sizeof(WNDCLASSEX), CS_HREDRAW | CS_VREDRAW, WndProc, 0, 0, hInstance, LoadIcon(NULL, IDI_APPLICATION), LoadCursor(NULL, IDC_ARROW), (HBRUSH)(COLOR_WINDOW + 1), NULL, L"FileSorterWin32", LoadIcon(NULL, IDI_APPLICATION) };
    if (!RegisterClassEx(&wcex)) { MessageBox(NULL, L"Window Registration Failed!", L"Error", MB_ICONEXCLAMATION | MB_OK); return 0; }
    g_hWnd = CreateWindow(L"FileSorterWin32", L"File Sorter (Win32)", WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, 800, 600, NULL, NULL, hInstance, NULL);
    if (!g_hWnd) { MessageBox(NULL, L"Window Creation Failed!", L"Error", MB_ICONEXCLAMATION | MB_OK); return 0; }
    ShowWindow(g_hWnd, nCmdShow); UpdateWindow(g_hWnd);
    MSG msg; while (GetMessage(&msg, NULL, 0, 0)) { TranslateMessage(&msg); DispatchMessage(&msg); }
    return (int)msg.wParam;
}

// Main window procedure
LRESULT CALLBACK WndProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    switch (uMsg) {
    case WM_CREATE:
        CreateControls(hwnd);
        wchar_t documentsPath[MAX_PATH];
        SHGetFolderPath(NULL, CSIDL_PERSONAL, NULL, 0, documentsPath);
        SetWindowText(g_hDirEdit, documentsPath);
        g_currentPath = documentsPath;
        PopulateTreeView(g_currentPath);
        return 0;
    case WM_COMMAND:
        if (LOWORD(wParam) == 1) {
            BROWSEINFO bi = { 0 }; bi.hwndOwner = hwnd; bi.lpszTitle = const_cast<LPWSTR>(L"Select a folder:"); bi.ulFlags = BIF_RETURNONLYFSDIRS | BIF_NEWDIALOGSTYLE;
            LPITEMIDLIST pidl = SHBrowseForFolder(&bi);
            if (pidl != NULL) {
                wchar_t path[MAX_PATH];
                if (SHGetPathFromIDList(pidl, path)) {
                    SetWindowText(g_hDirEdit, path);
                    g_currentPath = path;
                    PopulateTreeView(g_currentPath);
                }
                CoTaskMemFree(pidl);
            }
            return 0;
        }
        else if (LOWORD(wParam) == 2) {
            wchar_t path[MAX_PATH];
            GetWindowText(g_hDirEdit, path, MAX_PATH);
            g_currentPath = path;
            PopulateTreeView(g_currentPath);
            return 0;
        }
        break;
    case WM_NOTIFY:
        if (((LPNMHDR)lParam)->hwndFrom == g_hTreeView) {
            if (((LPNMHDR)lParam)->code == NM_DBLCLK) {
                HandleTreeViewClick((LPNMITEMACTIVATE)lParam);
                return 0;
            }
            else if (((LPNMHDR)lParam)->code == LVN_COLUMNCLICK) {
                LPNMLISTVIEW pnmv = (LPNMLISTVIEW)lParam;
                if (g_sortColumn == pnmv->iSubItem) g_sortAscending = !g_sortAscending;
                else { g_sortColumn = pnmv->iSubItem; g_sortAscending = true; }
                SortItems();
                PopulateTreeView(g_currentPath);
                return 0;
            }
        }
        break;
    case WM_SIZE:
        int width = LOWORD(lParam), height = HIWORD(lParam);
        RECT rcEdit; GetWindowRect(g_hDirEdit, &rcEdit);
        int editHeight = rcEdit.bottom - rcEdit.top;
        SendMessage(g_hStatusBar, WM_SIZE, 0, 0);
        SetWindowPos(g_hDirEdit, NULL, 10, 10, width - 190, editHeight, SWP_NOZORDER);
        SetWindowPos(GetDlgItem(hwnd, 1), NULL, width - 170, 10, 70, editHeight, SWP_NOZORDER);
        SetWindowPos(GetDlgItem(hwnd, 2), NULL, width - 90, 10, 70, editHeight, SWP_NOZORDER);
        RECT rcStatus; GetWindowRect(g_hStatusBar, &rcStatus);
        int statusHeight = rcStatus.bottom - rcStatus.top;
        SetWindowPos(g_hTreeView, NULL, 0, editHeight + 20, width, height - editHeight - 20 - statusHeight, SWP_NOZORDER);
        return 0;
    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
    }
    return DefWindowProc(hwnd, uMsg, wParam, lParam);
}

// Create all the controls for the application
void CreateControls(HWND hwnd) {
    g_hDirEdit = CreateWindowEx(WS_EX_CLIENTEDGE, L"EDIT", L"", WS_CHILD | WS_VISIBLE | ES_AUTOHSCROLL, 10, 10, 400, 25, hwnd, NULL, GetModuleHandle(NULL), NULL);
    CreateWindow(L"BUTTON", L"Browse", WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON, 420, 10, 70, 25, hwnd, (HMENU)1, GetModuleHandle(NULL), NULL);
    CreateWindow(L"BUTTON", L"Refresh", WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON, 500, 10, 70, 25, hwnd, (HMENU)2, GetModuleHandle(NULL), NULL);
    g_hTreeView = CreateWindowEx(WS_EX_CLIENTEDGE, WC_LISTVIEW, L"", WS_CHILD | WS_VISIBLE | LVS_REPORT | LVS_SHOWSELALWAYS | LVS_AUTOARRANGE, 0, 45, 0, 0, hwnd, NULL, GetModuleHandle(NULL), NULL);
    ListView_SetExtendedListViewStyle(g_hTreeView, LVS_EX_FULLROWSELECT | LVS_EX_GRIDLINES | LVS_EX_DOUBLEBUFFER);
    g_hStatusBar = CreateWindowEx(0, STATUSCLASSNAME, L"", WS_CHILD | WS_VISIBLE | SBARS_SIZEGRIP, 0, 0, 0, 0, hwnd, NULL, GetModuleHandle(NULL), NULL);
    LVCOLUMN lvc = { LVCF_FMT | LVCF_WIDTH | LVCF_TEXT | LVCF_SUBITEM, LVCFMT_LEFT, 250, const_cast<LPWSTR>(L"Name"), 0, 0 };
    ListView_InsertColumn(g_hTreeView, 0, &lvc);
    lvc.cx = 100; lvc.pszText = const_cast<LPWSTR>(L"Size"); ListView_InsertColumn(g_hTreeView, 1, &lvc);
    lvc.cx = 150; lvc.pszText = const_cast<LPWSTR>(L"Modified"); ListView_InsertColumn(g_hTreeView, 2, &lvc);
}

// Populate the tree view with files and directories
void PopulateTreeView(const std::wstring& path) {
    ListView_DeleteAllItems(g_hTreeView);
    g_fileItems.clear();
    if (!PathFileExists(path.c_str())) { MessageBox(g_hWnd, const_cast<LPWSTR>(L"The specified path does not exist."), const_cast<LPWSTR>(L"Error"), MB_ICONERROR | MB_OK); return; }
    std::wstring searchPath = path + L"\\*";
    WIN32_FIND_DATAW findData;
    HANDLE hFind = FindFirstFileW(searchPath.c_str(), &findData);
    if (hFind == INVALID_HANDLE_VALUE) { MessageBox(g_hWnd, const_cast<LPWSTR>(L"Unable to read directory contents."), const_cast<LPWSTR>(L"Error"), MB_ICONERROR | MB_OK); return; }
    do {
        std::wstring fileName = findData.cFileName;
        if (fileName == L"." || fileName == L"..") continue;
        FileItem item = { fileName, path + L"\\" + fileName, 0, findData.ftLastWriteTime, (findData.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) != 0 };
        if (!item.isDirectory) {
            ULARGE_INTEGER fileSize;
            fileSize.LowPart = findData.nFileSizeLow;
            fileSize.HighPart = findData.nFileSizeHigh;
            item.size = fileSize.QuadPart;
        }
        g_fileItems.push_back(item);
    } while (FindNextFileW(hFind, &findData));
    FindClose(hFind);
    SortItems();
    LVITEM lvi = { LVIF_TEXT | LVIF_PARAM | LVIF_IMAGE };
    for (size_t i = 0; i < g_fileItems.size(); i++) {
        const FileItem& item = g_fileItems[i];
        lvi.iImage = item.isDirectory ? 0 : 1;
        lvi.iItem = static_cast<int>(i);
        lvi.iSubItem = 0;
        lvi.pszText = const_cast<LPWSTR>(item.name.c_str());
        lvi.lParam = static_cast<LPARAM>(i);
        int idx = ListView_InsertItem(g_hTreeView, &lvi);
        std::wstring sizeStr = item.isDirectory ? L"<DIR>" : FormatFileSize(item.size);
        ListView_SetItemText(g_hTreeView, idx, 1, const_cast<LPWSTR>(sizeStr.c_str()));
        std::wstring dateStr = FormatFileTime(item.modified);
        ListView_SetItemText(g_hTreeView, idx, 2, const_cast<LPWSTR>(dateStr.c_str()));
    }
    RefreshStatusBar();
}
