import PropTypes from "prop-types";
import React, { useCallback } from "react";
import styled from "styled-components";

import style from "@agir/front/genericComponents/_variables.scss";
import { displayShortDate } from "@agir/lib/utils/time";

import Avatar from "@agir/front/genericComponents/Avatar";
import TextField from "@agir/front/formComponents/TextField";
import EmojiPicker from "@agir/front/formComponents/EmojiPicker";

const StyledLabel = styled.div``;
const StyledMessage = styled.div``;
const StyledWrapper = styled.div`
  padding: 1.5rem;

  ${StyledLabel} {
    display: flex;
    align-items: stretch;
    font-size: 0.875rem;
    margin-bottom: 1rem;

    ${Avatar} {
      flex: 0 0 auto;
      width: 2.5rem;
      height: 2.5rem;
      margin-top: 5px;
      margin-right: 0.5rem;
    }

    span {
      strong,
      em {
        display: block;
      }

      strong {
        font-weight: 600;
      }

      em {
        font-style: normal;
      }

      button {
        border: none;
        padding: 0;
        margin: 0;
        text-decoration: none;
        background: inherit;
        cursor: pointer;
        text-align: center;
        -webkit-appearance: none;
        -moz-appearance: none;
        color: ${style.primary500};

        &:focus,
        &:hover {
          border: none;
          outline: none;
          text-decoration: underline;
        }

        &[disabled] {
          &,
          &:hover,
          &:focus {
            opacity: 0.8;
            text-decoration: none;
            cursor: default;
          }
        }

        @media (max-width: ${style.collapse}px) {
          display: block;
        }
      }
    }
  }

  ${StyledMessage} {
    font-size: 1rem;

    textarea {
      max-height: 12rem;

      &,
      &:focus,
      &:hover {
        border: none;
        outline: none;
        padding-left: 0;
        padding-right: 0;
        font-size: 1rem;
        margin: 0;
        background-color: transparent;
      }
    }

    & > :last-child {
      @media (max-width: ${style.collapse}px) {
        display: none;
      }
    }
  }
`;

const MessageStep = (props) => {
  const {
    disabled,
    message,
    event,
    user,
    onChange,
    onClearEvent,
    maxLength,
  } = props;

  const handleInputChange = useCallback(
    (e) => {
      onChange(e.target.value);
    },
    [onChange]
  );

  const handleEmojiSelect = useCallback(
    (emoji) => {
      onChange(message + emoji);
    },
    [onChange, message]
  );

  return (
    <StyledWrapper>
      <StyledLabel>
        <Avatar name={user.fullName} avatar={user.avatar} />
        <span>
          <strong>{user.fullName}</strong>
          {event && event.name ? (
            <em>
              {`À propos de ${event.name}${
                event.startTime
                  ? " du " + displayShortDate(event.startTime)
                  : ""
              }`}
              &ensp;
              <button disabled={disabled} onClick={onClearEvent}>
                Changer
              </button>
            </em>
          ) : null}
        </span>
      </StyledLabel>
      <StyledMessage>
        <TextField
          textArea
          id="message"
          value={message}
          onChange={handleInputChange}
          autoFocus
          disabled={disabled}
          placeholder="Quoi de neuf dans votre groupe ?"
          maxLength={maxLength}
        />
        <EmojiPicker onSelect={handleEmojiSelect} />
      </StyledMessage>
    </StyledWrapper>
  );
};
MessageStep.propTypes = {
  disabled: PropTypes.bool,
  message: PropTypes.string,
  event: PropTypes.object,
  user: PropTypes.shape({
    fullName: PropTypes.string.isRequired,
    avatar: PropTypes.string,
  }).isRequired,
  onChange: PropTypes.func.isRequired,
  onClearEvent: PropTypes.func,
  maxLength: PropTypes.number,
};
export default MessageStep;
