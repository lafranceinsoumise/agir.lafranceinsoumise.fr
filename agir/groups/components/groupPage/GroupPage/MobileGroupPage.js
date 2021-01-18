import PropTypes from "prop-types";
import React, { useMemo } from "react";
import styled from "styled-components";

import style from "@agir/front/genericComponents/_variables.scss";

import { Column, Container, Row } from "@agir/front/genericComponents/grid";
import Skeleton from "@agir/front/genericComponents/Skeleton";
import Tabs from "@agir/front/genericComponents/Tabs";
import ShareCard from "@agir/front/genericComponents/ShareCard";

import GroupBanner from "../GroupBanner";

import GroupLocation from "../GroupLocation";
import GroupUserActions from "../GroupUserActions";
import GroupContactCard from "../GroupContactCard";
import GroupDescription from "../GroupDescription";
import GroupLinks from "../GroupLinks";
import GroupFacts from "../GroupFacts";
import GroupDonation from "../GroupDonation";
import GroupSuggestions from "../GroupSuggestions";
import GroupEventList from "../GroupEventList";

export const MobileGroupPageSkeleton = () => (
  <Container style={{ margin: "2rem auto", padding: "0 1rem" }}>
    <Row>
      <Column stack>
        <Skeleton />
      </Column>
    </Row>
  </Container>
);

const tabConfig = [
  {
    id: "info",
    label: "Présentation",
    isActive: true,
  },
  {
    id: "agenda",
    label: "Agenda",
    isActive: ({ pastEvents, upcomingEvents }) => {
      pastEvents = Array.isArray(pastEvents) ? pastEvents : [];
      upcomingEvents = Array.isArray(upcomingEvents) ? upcomingEvents : [];
      return pastEvents.length + upcomingEvents.length > 0;
    },
  },
];

const Tab = styled.div`
  max-width: 100%;
  margin: 0;
  padding: 0;
`;

const Agenda = styled.div`
  margin: 0;
  padding: 1.5rem 1rem;
  height: 316px;
  background: ${style.black25};

  & > h3 {
    margin-top: 0;
    margin-bottom: 1rem;
  }
`;

const MobileGroupPage = (props) => {
  const {
    group,
    groupSuggestions,
    upcomingEvents,
    pastEvents,
    isLoadingPastEvents,
    loadMorePastEvents,
  } = props;

  const tabs = useMemo(
    () =>
      tabConfig.filter((tab) =>
        typeof tab.isActive === "function" ? tab.isActive(props) : tab.isActive
      ),
    [props]
  );

  if (!group) {
    return null;
  }

  return (
    <Container
      style={{
        margin: 0,
        padding: "0 0 3.5rem",
      }}
    >
      <GroupBanner {...group} />
      <GroupUserActions {...group} />
      <Tabs tabs={tabs}>
        {({ handleNext }) => (
          <Tab>
            {Array.isArray(upcomingEvents) && upcomingEvents.length > 0 ? (
              <Agenda>
                <h3>Agenda</h3>
                <GroupEventList
                  events={[upcomingEvents[0]]}
                  loadMore={handleNext}
                  loadMoreLabel="Voir tout l'agenda"
                />
              </Agenda>
            ) : null}

            <GroupContactCard {...group} />
            <GroupDescription {...group} />
            <GroupLinks {...group} />
            <GroupFacts {...group} />
            <GroupLocation {...group} />
            {group.routes && group.routes.donations && (
              <GroupDonation url={group.routes.donations} />
            )}
            <ShareCard />

            {Array.isArray(groupSuggestions) && groupSuggestions.length > 0 ? (
              <div style={{ marginTop: 71, marginBottom: 71 }}>
                <GroupSuggestions groups={groupSuggestions} />
              </div>
            ) : null}
          </Tab>
        )}
        <Tab>
          <GroupEventList title="Événements à venir" events={upcomingEvents} />
          <GroupEventList
            title="Événements passés"
            events={pastEvents}
            loadMore={loadMorePastEvents}
            isLoading={isLoadingPastEvents}
          />
        </Tab>
      </Tabs>
    </Container>
  );
};
MobileGroupPage.propTypes = {
  group: PropTypes.shape({
    isMember: PropTypes.bool,
    isManager: PropTypes.bool,
    routes: PropTypes.shape({
      donations: PropTypes.string,
    }),
  }),
  groupSuggestions: PropTypes.arrayOf(PropTypes.object),
  upcomingEvents: PropTypes.arrayOf(PropTypes.object),
  pastEvents: PropTypes.arrayOf(PropTypes.object),
  isLoadingPastEvents: PropTypes.bool,
  loadMorePastEvents: PropTypes.func,
};
export default MobileGroupPage;