"""
Examples and sample data for the quicktype-mcp service.
This file contains sample JSON data and example Dart models for documentation and testing.
"""

# Sample JSON data for documentation and examples
SAMPLE_JSON = {
    "data": {
        "id": 101,
        "name": "Test User",
        "active": True,
        "created": "2023-10-15T08:30:00Z",
        "scores": [
            85.5,
            None,
            90
        ],
        "address": {
            "city": "San Francisco",
            "coordinates": {
                "lat": 37.7749,
                "lng": -122.4194
            }
        },
        "tags": [
            "user",
            "premium"
        ],
        "meta": {
            "devices": [
                "mobile",
                "desktop"
            ],
            "preferences": {
                "theme": "dark",
                "notifications": {
                    "email": True,
                    "push": None
                }
            },
            "lastSeen": "2023-10-20T14:00:00Z"
        },
        "groups": [
            {
                "id": 1,
                "name": "Admin"
            }
        ],
        "expires": None
    }
}

# Example of generated Dart model
SAMPLE_DART_MODEL = """
// To parse this JSON data, do
//
//     final sampleResponse = sampleResponseFromJson(jsonString);

import 'dart:convert';

SampleResponse sampleResponseFromJson(String str) => SampleResponse.fromJson(json.decode(str));

String sampleResponseToJson(SampleResponse data) => json.encode(data.toJson());

class SampleResponse {
    SampleResponseData? data;

    SampleResponse({
        this.data,
    });

    factory SampleResponse.fromJson(Map<String, dynamic> json) => SampleResponse(
        data: json["data"] == null ? null : SampleResponseData.fromJson(json["data"]),
    );

    Map<String, dynamic> toJson() => {
        "data": data?.toJson(),
    };
}

class SampleResponseData {
    int? id;
    String? name;
    bool? active;
    DateTime? created;
    List<double?>? scores;
    Address? address;
    List<String>? tags;
    Meta? meta;
    List<Group>? groups;
    dynamic expires;

    SampleResponseData({
        this.id,
        this.name,
        this.active,
        this.created,
        this.scores,
        this.address,
        this.tags,
        this.meta,
        this.groups,
        this.expires,
    });

    factory SampleResponseData.fromJson(Map<String, dynamic> json) => SampleResponseData(
        id: json["id"],
        name: json["name"],
        active: json["active"],
        created: json["created"] == null ? null : DateTime.parse(json["created"]),
        scores: json["scores"] == null ? [] : List<double?>.from(json["scores"]!.map((x) => x?.toDouble())),
        address: json["address"] == null ? null : Address.fromJson(json["address"]),
        tags: json["tags"] == null ? [] : List<String>.from(json["tags"]!.map((x) => x)),
        meta: json["meta"] == null ? null : Meta.fromJson(json["meta"]),
        groups: json["groups"] == null ? [] : List<Group>.from(json["groups"]!.map((x) => Group.fromJson(x))),
        expires: json["expires"],
    );

    Map<String, dynamic> toJson() => {
        "id": id,
        "name": name,
        "active": active,
        "created": created?.toIso8601String(),
        "scores": scores == null ? [] : List<dynamic>.from(scores!.map((x) => x)),
        "address": address?.toJson(),
        "tags": tags == null ? [] : List<dynamic>.from(tags!.map((x) => x)),
        "meta": meta?.toJson(),
        "groups": groups == null ? [] : List<dynamic>.from(groups!.map((x) => x.toJson())),
        "expires": expires,
    };
}

class Address {
    String? city;
    Coordinates? coordinates;

    Address({
        this.city,
        this.coordinates,
    });

    factory Address.fromJson(Map<String, dynamic> json) => Address(
        city: json["city"],
        coordinates: json["coordinates"] == null ? null : Coordinates.fromJson(json["coordinates"]),
    );

    Map<String, dynamic> toJson() => {
        "city": city,
        "coordinates": coordinates?.toJson(),
    };
}

class Coordinates {
    double? lat;
    double? lng;

    Coordinates({
        this.lat,
        this.lng,
    });

    factory Coordinates.fromJson(Map<String, dynamic> json) => Coordinates(
        lat: json["lat"]?.toDouble(),
        lng: json["lng"]?.toDouble(),
    );

    Map<String, dynamic> toJson() => {
        "lat": lat,
        "lng": lng,
    };
}

class Group {
    int? id;
    String? name;

    Group({
        this.id,
        this.name,
    });

    factory Group.fromJson(Map<String, dynamic> json) => Group(
        id: json["id"],
        name: json["name"],
    );

    Map<String, dynamic> toJson() => {
        "id": id,
        "name": name,
    };
}

class Meta {
    List<String>? devices;
    Preferences? preferences;
    DateTime? lastSeen;

    Meta({
        this.devices,
        this.preferences,
        this.lastSeen,
    });

    factory Meta.fromJson(Map<String, dynamic> json) => Meta(
        devices: json["devices"] == null ? [] : List<String>.from(json["devices"]!.map((x) => x)),
        preferences: json["preferences"] == null ? null : Preferences.fromJson(json["preferences"]),
        lastSeen: json["lastSeen"] == null ? null : DateTime.parse(json["lastSeen"]),
    );

    Map<String, dynamic> toJson() => {
        "devices": devices == null ? [] : List<dynamic>.from(devices!.map((x) => x)),
        "preferences": preferences?.toJson(),
        "lastSeen": lastSeen?.toIso8601String(),
    };
}

class Preferences {
    String? theme;
    Notifications? notifications;

    Preferences({
        this.theme,
        this.notifications,
    });

    factory Preferences.fromJson(Map<String, dynamic> json) => Preferences(
        theme: json["theme"],
        notifications: json["notifications"] == null ? null : Notifications.fromJson(json["notifications"]),
    );

    Map<String, dynamic> toJson() => {
        "theme": theme,
        "notifications": notifications?.toJson(),
    };
}

class Notifications {
    bool? email;
    dynamic push;

    Notifications({
        this.email,
        this.push,
    });

    factory Notifications.fromJson(Map<String, dynamic> json) => Notifications(
        email: json["email"],
        push: json["push"],
    );

    Map<String, dynamic> toJson() => {
        "email": email,
        "push": push,
    };
}
"""
