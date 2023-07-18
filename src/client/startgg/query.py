events_query = """
    query EventQuery(
        $slug: String 
        $filters: SetFilters
        $page: Int
        $sortType: SetSortType
    ) {
        event(slug: $slug) {
            id
            slug
            updatedAt
            sets(filters: $filters page: $page sortType: $sortType) {
                pageInfo {
                    total
                    totalPages
                    page
                    perPage
                    sortBy
                    filter
                }
                nodes {
                    id
                    completedAt
                    games {
                        id
                        winnerId
                        orderNum
                        selections {
                            orderNum
                            selectionType
                            selectionValue
                            entrant {
                                id
                                name
                                initialSeedNum
                                standing {
                                    isFinal
                                    placement
                                }
                            }
                        }
                    }
                    identifier
                    displayScore
                    fullRoundText
                    totalGames
                    lPlacement
                    wPlacement
                    winnerId
                    state
                    setGamesType
                    round
                    phaseGroup {
                        displayIdentifier
                    }
                    slots {
                        entrant {
                            id
                            name
                            initialSeedNum
                            standing {
                                isFinal
                                placement
                            }
                        }
                    }
                }
            }
        }
    }
"""

characters_query = """
    query CharactersQuery(
        $slug: String
    ) {
        videogame(slug: $slug) {
            id
            slug
            characters {
                id
                name
            }
        }
    }
"""
