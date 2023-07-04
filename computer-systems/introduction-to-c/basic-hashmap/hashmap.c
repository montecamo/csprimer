#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define STARTING_BUCKETS 8
#define MAX_KEY_SIZE 32

typedef struct Entry {
  char *key;
  void *value;
} Entry;

typedef struct Node {
  void *value;
  struct Node *next;
} Node;

typedef struct LinkedList {
  Node *head;
} LinkedList;

typedef struct HashMap {
  LinkedList **buckets;
} HashMap;

Entry *make_entry(char *key, void *value) {
  Entry *entry = malloc(sizeof(Entry));

  entry->key = key;
  entry->value = value;

  return entry;
}

void free_entry(Entry *entry) { free(entry); }

LinkedList *make_linkedlist() {
  LinkedList *list = malloc(sizeof(LinkedList));

  list->head = NULL;

  return list;
}

void push_linkedlist(LinkedList *list, void *value) {
  Node *node = malloc(sizeof(Node));
  node->value = value;
  node->next = NULL;

  if (list->head == NULL) {
    list->head = node;
  } else {
    Node *last = list->head;

    while (last->next != NULL) {
      last = last->next;
    }

    last->next = node;
  }
}

void free_linkedlist(LinkedList *list) {
  Node *node = list->head;
  Node *next = NULL;

  while (next != NULL) {
    next = node->next;

    free_entry((Entry *)node->value);
    free(node);
  }

  free(list);
}

HashMap *make_hashmap() {
  HashMap *map = malloc(sizeof(HashMap));

  map->buckets = malloc(sizeof(LinkedList) * STARTING_BUCKETS);

  for (int i = 0; i < STARTING_BUCKETS; i++) {
    map->buckets[i] = make_linkedlist();
  }

  return map;
}

int hash(char *value) {
  int h = 0;

  int len = strlen(value);

  for (int i = 0; i < len; i++) {
    h += value[i];
  }

  return h % STARTING_BUCKETS;
}

Entry *Hashmap_get_entry(HashMap *map, char *key) {
  Node *node = map->buckets[hash(key)]->head;

  while (node != NULL) {
    Entry *entry = (Entry *)node->value;

    if (strcmp(entry->key, key) == 0) {
      return entry;
    }

    node = node->next;
  }

  return NULL;
}

void *Hashmap_get(HashMap *map, char *key) {
  Entry *entry = Hashmap_get_entry(map, key);

  if (entry != NULL) {
    return entry->value;
  }

  return NULL;
}

void Hashmap_set(HashMap *map, char *key, void *value) {
  char *key_copy = malloc(sizeof(char) * strlen(key));
  strcpy(key_copy, key);

  Entry *entry = Hashmap_get_entry(map, key_copy);

  if (entry == NULL) {
    push_linkedlist(map->buckets[hash(key_copy)], make_entry(key_copy, value));
  } else {
    entry->value = value;
  }
}

void Hashmap_delete(HashMap *map, char *key) {
  Node *previous = NULL;
  LinkedList *list = map->buckets[hash(key)];
  Node *node = list->head;

  while (node != NULL) {
    Entry *entry = (Entry *)node->value;

    if (strcmp(entry->key, key) == 0) {
      if (previous == NULL) {
        list->head = NULL;
      } else {
        previous->next = node->next;
      }

      free(entry);
      free(node);

      break;
    }

    previous = node;
    node = node->next;
  }
}

void Hashmap_free(HashMap *map) {
  for (int i = 0; i < STARTING_BUCKETS; i++) {
    free_linkedlist(map->buckets[i]);
  }

  free(map->buckets);
  free(map);
}

int main() {
  HashMap *h = make_hashmap();

  // basic get/set functionality
  int a = 5;
  float b = 7.2;
  Hashmap_set(h, "item a", &a);
  Hashmap_set(h, "item b", &b);
  assert(Hashmap_get(h, "item a") == &a);
  assert(Hashmap_get(h, "item b") == &b);

  // using the same key should override the previous value
  int c = 20;
  Hashmap_set(h, "item a", &c);
  assert(Hashmap_get(h, "item a") == &c);

  // basic delete functionality
  Hashmap_delete(h, "item a");
  assert(Hashmap_get(h, "item a") == NULL);

  // handle collisions correctly
  // note: this doesn't necessarily test expansion
  int i, n = STARTING_BUCKETS * 10, ns[n];
  char key[MAX_KEY_SIZE];
  for (i = 0; i < n; i++) {
    ns[i] = i;
    sprintf(key, "item %d", i);
    Hashmap_set(h, key, &ns[i]);
  }

  for (i = 0; i < n; i++) {
    sprintf(key, "item %d", i);
    assert(Hashmap_get(h, key) == &ns[i]);
  }

  Hashmap_free(h);
  /*
     stretch goals:
     - expand the underlying array if we start to get a lot of collisions
     - support non-string keys
     - try different hash functions
     - switch from chaining to open addressing
     - use a sophisticated rehashing scheme to avoid clustered collisions
     - implement some features from Python dicts, such as reducing space use,
     maintaing key ordering etc. see https://www.youtube.com/watch?v=npw4s1QTmPg
     for ideas
     */
  printf("ok\n");
}
