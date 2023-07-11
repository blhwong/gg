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