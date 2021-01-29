import PropTypes from "prop-types";
import React, { useCallback, useEffect, useMemo, useRef } from "react";
import styled from "styled-components";

import { FaWhatsapp, FaTelegram, FaFacebook, FaTwitter } from "react-icons/fa";

import style from "@agir/front/genericComponents/_variables.scss";
import { timeAgo } from "@agir/lib/utils/time";
import { formatEvent } from "@agir/events/common/utils";
import useCopyToClipboard from "@agir/front/genericComponents/useCopyToClipboard";

import Avatar from "@agir/front/genericComponents/Avatar";
import Card from "@agir/front/genericComponents/Card";
import EventCard from "@agir/front/genericComponents/EventCard";
import InlineMenu from "@agir/front/genericComponents/InlineMenu";
import PageFadeIn from "@agir/front/genericComponents/PageFadeIn";
import { RawFeatherIcon } from "@agir/front/genericComponents/FeatherIcon";
import { ResponsiveLayout } from "@agir/front/genericComponents/grid";

import CommentField, {
  CommentButton,
} from "@agir/front/formComponents/CommentField";
import Comment from "@agir/front/formComponents/Comment";

const StyledInlineMenuItems = styled.div`
  cursor: pointer;
  display: flex;
  flex-flow: column nowrap;
  align-items: stretch;
  list-style: none;
  color: ${style.primary500};
  padding: 0;

  @media (max-width: ${style.collapse}px) {
    margin: 0;
    padding: 1.5rem;
  }

  a,
  button {
    display: flex;
    align-items: center;
    border: none;
    padding: 0;
    margin: 0;
    text-decoration: none;
    background: inherit;
    cursor: pointer;
    text-align: center;
    -webkit-appearance: none;
    -moz-appearance: none;
    font-size: 0.875rem;
    line-height: 20px;
    font-weight: 400;
    color: ${style.black1000};
    margin-bottom: 0.5rem;

    &:last-child {
      margin-bottom: 0;
    }

    &:hover,
    &:focus {
      text-decoration: underline;
      border: none;
      outline: none;
    }

    &[disabled],
    &[disabled]:hover,
    &[disabled]:focus {
      opacity: 0.75;
      text-decoration: none;
      cursor: default;
    }

    @media (max-width: ${style.collapse}px) {
      margin-bottom: 1.5rem;
      text-decoration: none;
    }

    & > *:first-child {
      margin-right: 0.5rem;
      width: 1rem;
      height: 1rem;

      @media (max-width: ${style.collapse}px) {
        margin-right: 1rem;
        width: 1.5rem;
        height: 1.5rem;
      }

      svg {
        width: inherit;
        height: inherit;
        stroke-width: 2;
      }
    }
  }
`;
const StyledAction = styled.div`
  & > button {
    border: none;
    padding: 0;
    margin: 0;
    text-decoration: none;
    background: inherit;
    cursor: pointer;
    text-align: center;
    -webkit-appearance: none;
    -moz-appearance: none;
  }
`;
const StyledContent = styled.div`
  padding: 0;
  font-size: inherit;
  line-height: 1.65;

  @media (max-width: ${style.collapse}px) {
    font-size: 0.875rem;
    line-height: 1.6;
  }

  span {
    display: block;
    min-height: 1em;
    font-size: inherit;
    line-height: inherit;
  }
`;
const StyledHeader = styled.div`
  display: flex;
  flex-flow: row nowrap;
  align-items: flex-start;
  font-size: 1rem;
  margin-bottom: 0.5rem;
  padding: 0;
  line-height: 1.4;

  & > ${Avatar} {
    flex: 0 0 auto;
    width: 2.5rem;
    height: 2.5rem;
    margin-right: 0.5rem;

    @media (min-width: ${style.collapse}px) {
      display: none;
    }
  }

  h4 {
    margin: 0;
    flex-grow: 1;
    font-size: inherit;
    display: flex;
    flex-flow: row nowrap;

    @media (max-width: ${style.collapse}px) {
      flex-flow: column nowrap;
    }

    strong {
      font-weight: 600;
      font-size: inherit;
    }

    em {
      font-style: normal;
      font-weight: normal;
      font-size: inherit;
      color: ${style.black500};
      margin-left: 0.5rem;

      @media (max-width: ${style.collapse}px) {
        margin-left: 0;
        margin-top: 0.25rem;
        font-size: 0.875rem;
      }
    }
  }

  ${StyledAction} {
    & > * {
      margin-left: 0.5rem;
    }

    ${RawFeatherIcon} {
      width: 1rem;
      height: 1rem;

      svg {
        width: inherit;
        height: inherit;
        stroke-width: 2;
      }
    }
  }
`;
const StyledCommentCount = styled.p`
  display: flex;
  flex-flow: row nowrap;
  align-items: center;
  color: ${style.primary500};
  font-size: 0.875rem;
  font-weight: 500;

  ${RawFeatherIcon} {
    width: 1rem;
    height: 1rem;
  }
`;
const StyledComments = styled.div`
  && > * {
    margin-top: 1rem;

    &:first-child {
      margin-top: 0;
    }
  }
`;
const StyledMessage = styled.div``;
const StyledWrapper = styled.div`
  width: 100%;
  padding: 2.5rem 0;
  margin: 0;
  display: flex;
  flex-flow: row nowrap;
  align-items: flex-start;
  background-color: white;
  scroll-margin-top: 160px;

  @media (max-width: ${style.collapse}px) {
    scroll-margin-top: 120px;
    padding: 1.5rem 1rem;
    box-shadow: ${style.elaborateShadow};
  }

  & + & {
    border-top: 1px solid ${style.black100};

    @media (max-width: ${style.collapse}px) {
      padding-top: 1.5rem;
      margin-top: 1rem;
      border-top: none;
    }
  }

  & > ${Avatar} {
    flex: 0 0 auto;
    width: 2.5rem;
    height: 2.5rem;
    margin-right: 1rem;

    @media (max-width: ${style.collapse}px) {
      display: none;
    }
  }

  ${StyledMessage} {
    flex: 1 1 auto;

    & > * {
      margin-top: 1rem;
      margin-bottom: 0;

      &:first-child,
      &:empty {
        margin-top: 0;
      }
    }

    ${Card} {
      @media (max-width: ${style.collapse}px) {
        box-shadow: none;
        border: 1px solid ${style.black100};
      }
    }
  }
`;

const MessageCard = (props) => {
  const {
    user,
    message,
    messageURL,
    comments,
    isLoading,
    onClick,
    onComment,
    onDelete,
    onEdit,
    onReport,
    withMobileCommentField,
    scrollIn,
  } = props;

  const { author, content, created, linkedEvent, commentCount } = message;

  const messageCardRef = useRef();

  const event = useMemo(() => formatEvent(linkedEvent), [linkedEvent]);
  const isAuthor = useMemo(() => author.id === user.id, [author, user]);
  const encodedMessageURL = useMemo(() => {
    if (messageURL) {
      const url =
        window &&
        window.location &&
        window.location.origin &&
        !messageURL.includes("http")
          ? window.location.origin + messageURL
          : messageURL;

      return encodeURIComponent(url);
    }
  }, [messageURL]);
  const [isURLCopied, copyURL] = useCopyToClipboard(encodedMessageURL);

  const hasActions = useMemo(
    () =>
      isAuthor
        ? typeof onEdit === "function" || typeof onDelete === "function"
        : typeof onReport === "function",
    [isAuthor, onEdit, onDelete, onReport]
  );

  const handleClick = useCallback(() => {
    onClick && onClick(message);
  }, [message, onClick]);

  const handleEdit = useCallback(() => {
    onEdit && onEdit(message);
  }, [message, onEdit]);

  const handleDelete = useCallback(() => {
    onDelete && onDelete(message);
  }, [message, onDelete]);

  const handleReport = useCallback(() => {
    onReport && onReport(message);
  }, [message, onReport]);

  const handleComment = useCallback(
    (comment) => {
      onComment && onComment(comment, message);
    },
    [message, onComment]
  );
  const handleDeleteComment = useCallback(
    (comment) => {
      onDelete && onDelete(comment, message);
    },
    [message, onDelete]
  );

  useEffect(() => {
    scrollIn &&
      messageCardRef.current &&
      messageCardRef.current.scrollIntoView &&
      messageCardRef.current.scrollIntoView();
  }, [scrollIn]);

  return (
    <StyledWrapper ref={messageCardRef}>
      <Avatar {...author} />
      <StyledMessage>
        <StyledHeader>
          <Avatar {...author} />
          <h4>
            <strong>{author.fullName}</strong>
            <em onClick={handleClick} style={{ cursor: "pointer" }}>
              {created ? timeAgo(created) : null}
            </em>
          </h4>
          <StyledAction>
            {encodedMessageURL ? (
              <InlineMenu triggerIconName="share-2" triggerSize="1rem">
                <StyledInlineMenuItems>
                  <a href={`https://t.me/share/url?url=${encodedMessageURL}`}>
                    <FaTelegram color={style.primary500} />
                    Telegram
                  </a>
                  <a
                    href={`https://www.facebook.com/sharer/sharer.php?u=${encodedMessageURL}`}
                  >
                    <FaFacebook color={style.primary500} />
                    Facebook
                  </a>
                  <a
                    href={`https://twitter.com/intent/tweet?text=${encodedMessageURL}`}
                  >
                    <FaTwitter color={style.primary500} />
                    Twitter
                  </a>
                  <a href={`https://wa.me/?text=${encodedMessageURL}`}>
                    <FaWhatsapp color={style.primary500} />
                    Whatsapp
                  </a>
                  <button onClick={copyURL}>
                    <RawFeatherIcon
                      name={isURLCopied ? "check" : "copy"}
                      color={style.primary500}
                    />
                    {isURLCopied ? "Lien copié" : "Copier le lien"}
                  </button>
                </StyledInlineMenuItems>
              </InlineMenu>
            ) : null}
            {hasActions ? (
              <InlineMenu
                triggerIconName="more-horizontal"
                triggerSize="1rem"
                shouldDismissOnClick
              >
                <StyledInlineMenuItems>
                  {isAuthor && onEdit && (
                    <button onClick={handleEdit} disabled={isLoading}>
                      <RawFeatherIcon name="edit-2" color={style.primary500} />
                      Modifier
                    </button>
                  )}
                  {isAuthor && onDelete && (
                    <button onClick={handleDelete} disabled={isLoading}>
                      <RawFeatherIcon name="x" color={style.primary500} />
                      Supprimer
                    </button>
                  )}
                  {!isAuthor && onReport && (
                    <button onClick={handleReport} disabled={isLoading}>
                      <RawFeatherIcon name="flag" color={style.primary500} />
                      Signaler
                    </button>
                  )}
                </StyledInlineMenuItems>
              </InlineMenu>
            ) : null}
          </StyledAction>
        </StyledHeader>
        <StyledContent>
          {content.split("\n").map((paragraph, i) => (
            <span key={i + "__" + paragraph}>{paragraph}</span>
          ))}
        </StyledContent>
        {event ? <EventCard {...event} /> : null}
        {typeof commentCount === "number" && commentCount > 1 ? (
          <StyledCommentCount
            onClick={handleClick}
            style={{ cursor: "pointer" }}
          >
            <RawFeatherIcon name="message-circle" color={style.primary500} />
            &ensp;{commentCount} commentaires
          </StyledCommentCount>
        ) : null}
        <StyledComments>
          <PageFadeIn ready={Array.isArray(comments) && comments.length > 0}>
            {Array.isArray(comments) && comments.length > 0
              ? comments.map((comment) => (
                  <Comment
                    key={comment.id}
                    message={comment}
                    onDelete={handleDeleteComment}
                    onReport={onReport}
                    isAuthor={comment.author.id === user.id}
                  />
                ))
              : null}
          </PageFadeIn>
          {onComment ? (
            withMobileCommentField ? (
              <CommentField
                key={comments.length}
                isLoading={isLoading}
                user={user}
                onSend={handleComment}
              />
            ) : (
              <ResponsiveLayout
                MobileLayout={CommentButton}
                DesktopLayout={CommentField}
                key={comments.length}
                isLoading={isLoading}
                user={user}
                onSend={handleComment}
                onClick={onClick && handleClick}
              />
            )
          ) : null}
        </StyledComments>
      </StyledMessage>
    </StyledWrapper>
  );
};
MessageCard.propTypes = {
  user: PropTypes.shape({
    id: PropTypes.string.isRequired,
    avatar: PropTypes.string,
  }).isRequired,
  message: PropTypes.shape({
    id: PropTypes.string.isRequired,
    author: PropTypes.shape({
      id: PropTypes.string.isRequired,
      fullName: PropTypes.string.isRequired,
      avatar: PropTypes.string,
    }).isRequired,
    created: PropTypes.string.isRequired,
    content: PropTypes.string.isRequired,
    linkedEvent: PropTypes.object,
    commentCount: PropTypes.number,
  }).isRequired,
  messageURL: PropTypes.string,
  comments: PropTypes.arrayOf(PropTypes.object),
  onClick: PropTypes.func,
  onComment: PropTypes.func,
  onDelete: PropTypes.func,
  onEdit: PropTypes.func,
  onReport: PropTypes.func,
  isLoading: PropTypes.bool,
  withMobileCommentField: PropTypes.bool,
  scrollIn: PropTypes.bool,
};
export default MessageCard;