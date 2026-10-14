# UC-04: Bookmark & Organize Case Studies
*Diagram Type: UML Activity Diagram (Client Storage & Telemetry Signal)*

Models bookmark toggling, folder classification, PWA offline synchronization, and telemetry dispatch.

```mermaid
flowchart TD
    Start([User Taps Bookmark Icon on Card]) --> CheckBookmarkStatus{Already Bookmarked?}
    
    CheckBookmarkStatus -- No --> CreateBookmark[Generate Bookmark Record & Timestamp]
    CreateBookmark --> UpdateUI[Toggle Icon to Active Gold State]
    UpdateUI --> DispatchTelemetry[Dispatch 5x Weight Telemetry Event to UC-17 CAS Engine]
    DispatchTelemetry --> SaveOffline{PWA Offline Caching Enabled?}
    SaveOffline -- Yes --> CacheAssets[Cache Card Slides & Metadata into Local IndexedDB Storage]
    SaveOffline -- No --> PromptCollection[Prompt User: Add to Folder/Collection?]
    CacheAssets --> PromptCollection
    
    PromptCollection -- Select Existing Folder --> AssignFolder[Link Bookmark to Named Folder]
    PromptCollection -- Create New Folder --> CreateFolder[Create New Named Folder & Link]
    PromptCollection -- Dismiss / Default --> AssignDefault[Store in 'All Bookmarks' Default Collection]
    
    CheckBookmarkStatus -- Yes --> PromptRemove[Confirm Remove Bookmark]
    PromptRemove -- Yes --> DeleteBookmark[Remove Record from DB and IndexedDB]
    DeleteBookmark --> RevertUI[Revert Icon to Inactive State]
    RevertUI --> DecrementTelemetry[Adjust Telemetry Signals]
```
