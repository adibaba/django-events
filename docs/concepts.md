# Concepts - Documentation - Django Event Management

Contents:

- [User roles](#user-roles)
- [Event states](#event-states)
- [Registration states](#registration-states)

## User roles

Also see: `User`, `Person` and `Group` in the [Models](models.md)

### Superusers

- Permissions to administrate all data
- Created by shell command or by other *superusers* using the Django Admin user flag "Superuser status"

### Moderators

- Permissions to set *supervisors* for all *users*
- Permissions to edit constants (`Country`, `Level`, `Unit`)
- Created by *superusers* in Django Admin: Add user to group "moderators" (sets permissions) and set flag "Staff status" (allows to use Django Admin)

### Supervisors

- Permissions to approve event registrations for:
  - *Users* for whom the current user is registered as direct *supervisor*
  - *Users* of other *supervisors*, if those set the current user as representatives
- Permissions to set other representatives, which have to be *supervisors*, too
- Created by *moderators* or *superusers* by setting the field "representatives" of persons

### Users/Persons

- Permissions to create events and to register for events of others
- Created by themselfes
- Note: In the database model, each User instance has exactly one related Person instance

## Event states

Also see: `Event` in the [Models](models.md)

An event has the following properties which affect registrations:

- Time:
  - `date`, `time_begin` and `duration` (integer, in minutes)
  - Resulting in the states *upcoming/current* events and *past* events
- `maximum_participants` (integer)
  - Affects the registration state *free slots*
- `leisure` (boolean)
  - Leisure/free time: No registration required
  - Working time: Registration required
- `published` (boolean)
  - If set:
    - Registrations are possible
    - If there are registrations, this can not be unset anymore
- `canceled` (boolean)
  - If set: No additional registrations are possible

## Registration states

- Also see: `Registration` in the [Models](models.md)
- Registrations for events are possible, if all of the following conditions of an event are given:
  - The event is in working time (for leisure time, no registration is required)
  - The event has been published
  - The event has not been canceled
  - The event has free slots (maximum_participants < number of registrations)
  - The event is not in the past
- A registration has the following proprties:
  - `approvement_state` (True, False, unknown)
    - True: A registration has been approved
    - False: A registration was rejected
    - Unknown: The approvement decision has not been done
  - `canceled` (boolean)
    - If set, no registrations are possible

### Free slots

The total number of available event slots is set by `Event.maximum_participants`.  
Each new registration blocks an event slot.  
A registration stops blocking an event slot, if it is canceled by the participant.  
It also stops blocking, if the event is in working time and rejected by a supervisor.

Free slots of an event can be detemined by:  
`Event.maximum_participants` -  
number of related registrations with  
`Registration.canceled == False` OR  
(`Event.leisure == False` AND `Registration.approvement_state != False`)

### Corner cases for registrations

The default case is that all states of events (and registration approvals) are initially set and not modified.
In those settings it is easy to determine e.g. if there are free slots left.
On state changes, some of the corner cases below may occur.

- "Presenter unpublishes event" (**PUE**):
  - Setting: A presenter created and published an event. Now, she wants to withdraw the publication, but users already registered.
  - Handling:
    - Backend: Check publication state and registrations.  
      Message: "You can not withdraw the publication of your event as persons already registered. (You could cancel your event or edit it.)" ([EventForm](../events/forms.py))
    - Frontend: Prevent the action. Disable field if there are registrations. ([EventForm](../events/forms.py))
- "User withdraws cancelation" (**UWC**):
  - Setting : A person canceled her registration in the past.
  Now, the person wants to withdraw a previous cancelation of a registration.
  But there are no free slots.
  - Handling:
    - Backend: Check free slots and display message "There are no free slots" ([registration_create_view](../events/views.py))
    - Frontend: Prevent the action. Disable button to re-attend event. ([event_detail](../events/templates/events/event_detail.html))
- "Supervisor approves registration" (**SAR**):
  - Setting: A supervisor wants to approve a registration, but there are no free slots.
  - Note: This should never happen in practice, as slots are reserved even if registrations are not approved.
  - Handling:
    - Backend: Check free slots and display message "You can not withdraw your rejection as there are no free slots left for the event." ([registration_approval_view](../events/views.py))
    - Frontend: Prevent the action. Disable button to approve event. ([approvals](../events/templates/events/approvals.html))

## Update states

The event update form properties reflect the following states.

An event can be published (p), canceled (c) and can have registrations (r).

The resulting forms show some properties and allow related actions.

| Update state    | Event       | Show | Actions        |
|-----------------|-------------|------|----------------|
| 1 Create        | p:n c:n r:n | -    | Save      -> 2 |
| 2 Draft         | p:n c:n r:n | p    | Save, p:y -> 3 |
| 3 Published     | p:y c:n r:n | p    | Save, p:n -> 2 |
| 4 Registrations | p:y c:n r:y | c    | Save, c:y -> 5 |
| 5 Canceled      | p:y c:y r:y | -    | Save           |
